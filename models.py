from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, doctor, nurse, staff, finance, patient
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    doctor_appointments = db.relationship('Appointment', backref='doctor', foreign_keys='Appointment.doctor_id')
    patient_appointments = db.relationship('Appointment', backref='patient_rel', foreign_keys='Appointment.patient_id')

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
    blood_type = db.Column(db.String(5))
    height = db.Column(db.Integer)  # in cm
    weight = db.Column(db.Float)    # in kg
    allergies = db.Column(db.Text)

    user = db.relationship('User', backref='patient_profile')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Doctor is a User with role='doctor'
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, Completed, Cancelled

    # Relationships
    patient = db.relationship('Patient', backref='appointments', foreign_keys=[patient_id])
class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    admission_date = db.Column(db.DateTime, nullable=False)
    discharge_date = db.Column(db.DateTime)
    room_number = db.Column(db.String(20))
    bed_number = db.Column(db.String(20))
    diagnosis = db.Column(db.Text)
    status = db.Column(db.String(20), default='Admitted')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_name = db.Column(db.String(100), nullable=False)
    test_date = db.Column(db.DateTime, nullable=False)
    result = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StaffSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shift_start = db.Column(db.DateTime, nullable=False)
    shift_end = db.Column(db.DateTime, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    admission_id = db.Column(db.Integer, db.ForeignKey('admission.id'))
    amount = db.Column(db.Float, nullable=False)
    date_issued = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    insurance_claim = db.Column(db.Boolean, default=False)
    insurance_provider = db.Column(db.String(100))
    claim_status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    staff_id = db.Column(db.String(50), unique=True, nullable=False)
    department = db.Column(db.String(50), nullable=True)
    position = db.Column(db.String(50), nullable=False)
    user = db.relationship('User', backref=db.backref('staff', lazy=True))
