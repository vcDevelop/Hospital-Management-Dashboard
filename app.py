from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, doctor, nurse, staff, finance, patient
    department = db.Column(db.String(50))  # New department field
    position = db.Column(db.String(50))  # New department field
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ... rest of your User model ...

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    medical_history = db.Column(db.Text)
    address = db.Column(db.String(200))

    user = db.relationship('User', backref='patient_profile')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.Text, nullable=False)

    patient = db.relationship('Patient', backref='appointments')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role in ['doctor', 'nurse']:
            return redirect(url_for('patient_dashboard'))
        elif current_user.role == 'staff':
            return redirect(url_for('staff_dashboard'))
        elif current_user.role == 'finance':
            return redirect(url_for('financial_dashboard'))
        elif current_user.role == 'patient':
            return redirect(url_for('patient_portal'))
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            new_user = User(
                username=request.form['username'],
                email=request.form['email'],
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                phone=request.form.get('phone'),
                role=request.form['role'],
                department=request.form.get('department'),
                position=request.form.get('position')   # Add department field
            )
            
            new_user.set_password(request.form['password'])
            db.session.add(new_user)
            db.session.flush()

            if request.form['role'] == 'patient':
                patient = Patient(
                    user_id=new_user.id,
                    dob=datetime.strptime(request.form['dob'], '%Y-%m-%d').date(),
                    gender=request.form['gender'],
                    medical_history=request.form.get('medical_history'),
                    address=request.form.get('address')
                )
                db.session.add(patient)

            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        selected_role = request.form.get('role')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
            
        if user.role != selected_role:
            flash(f'Please login as {user.role}', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        flash('Login successful!', 'success')

        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Dashboards
@app.route('/admin-dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route("/patient_dashboard")
@login_required
def patient_dashboard():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    appointments = Appointment.query.filter_by(patient_id=current_user.id).order_by(Appointment.appointment_date).all()

    if not patient:
        flash("Patient record not found!", "danger")
        return redirect(url_for("login"))  # Redirect to home if patient doesn't exist
    return render_template("patient/dashboard.html", patient=patient, appointments=appointments)


@app.route('/staff-dashboard')
@login_required
def staff_dashboard():
    return render_template('staff/dashboard.html')

@app.route('/financial-dashboard')
@login_required
def financial_dashboard():
    return render_template('financial/dashboard.html')

@app.route('/patient-portal')
@login_required
def patient_portal():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    appointments = Appointment.query.filter_by(patient_id=patient.id).all() if patient else []
    return render_template('patient/dashboard.html', patient=patient, appointments=appointments)

@app.route("/delete_appointment", methods=["POST"])
@login_required
def delete_appointment():
    appointment_id = request.form.get("appointment_id")
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        flash("Appointment not found!", "danger")
        return redirect(url_for("patient_dashboard"))

    # Ensure only the correct patient can delete their own appointment
    if appointment.patient_id != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("patient_dashboard"))

    db.session.delete(appointment)
    db.session.commit()
    flash("Appointment deleted successfully!", "success")
    return redirect(url_for("patient_dashboard"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('public/404.html'), 404

# Appointment Booking
@app.route('/add_appointment', methods=['POST'])
@login_required
def add_appointment():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    if not patient:
        flash('Patient profile not found!', 'danger')
        return redirect(url_for('patient_portal'))

    date_str = request.form['appointment_date']
    time_str = request.form['appointment_time']
    reason = request.form['reason']

    appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    if appointment_date < datetime.today().date():
        flash('Invalid date! You cannot select past dates.', 'danger')
        return redirect(url_for('patient_portal'))

    appointment = Appointment(
        patient_id=patient.id,
        appointment_date=appointment_date,
        appointment_time=datetime.strptime(time_str, '%H:%M').time(),
        reason=reason
    )

    db.session.add(appointment)
    db.session.commit()
    flash('Appointment booked successfully!', 'success')
    return redirect(url_for('patient_portal'))

# Error Handlers
@app.errorhandler(403)
def forbidden(e):
    return render_template('public/403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('public/404.html'), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

