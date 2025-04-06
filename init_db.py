# from app import app, db
# from models import User, Patient, Appointment, Admission, TestResult, StaffSchedule, Attendance, Billing
# from werkzeug.security import generate_password_hash
# from datetime import datetime, timedelta

# def create_sample_data():
#     # Clear existing data
#     db.drop_all()
#     db.create_all()

#     # Create admin user
#     admin = User(
#         username='admin',
#         password=generate_password_hash('admin123', method='sha256'),
#         role='admin'
#     )
#     db.session.add(admin)
    
#     # Create doctors
#     doctor1 = User(
#         username='dr_smith',
#         password=generate_password_hash('doctor123', method='sha256'),
#         role='doctor'
#     )
#     doctor2 = User(
#         username='dr_jones',
#         password=generate_password_hash('doctor123', method='sha256'),
#         role='doctor'
#     )
#     db.session.add(doctor1)
#     db.session.add(doctor2)
    
#     # Create staff
#     nurse1 = User(
#         username='nurse_amy',
#         password=generate_password_hash('nurse123', method='sha256'),
#         role='nurse'
#     )
#     staff1 = User(
#         username='staff_mike',
#         password=generate_password_hash('staff123', method='sha256'),
#         role='staff'
#     )
#     finance1 = User(
#         username='finance_john',
#         password=generate_password_hash('finance123', method='sha256'),
#         role='finance'
#     )
#     db.session.add(nurse1)
#     db.session.add(staff1)
#     db.session.add(finance1)
    
#     # Create patients
#     patient1 = Patient(
#         first_name='John',
#         last_name='Doe',
#         dob=datetime(1980, 5, 15),
#         gender='Male',
#         address='123 Main St, Anytown',
#         phone='555-0101',
#         email='john.doe@example.com',
#         blood_type='A+',
#         allergies='Penicillin'
#     )
#     patient2 = Patient(
#         first_name='Jane',
#         last_name='Smith',
#         dob=datetime(1975, 8, 22),
#         gender='Female',
#         address='456 Oak Ave, Somewhere',
#         phone='555-0202',
#         email='jane.smith@example.com',
#         blood_type='O-',
#         allergies='None'
#     )
#     db.session.add(patient1)
#     db.session.add(patient2)
    
#     # Create appointments
#     appt1 = Appointment(
#         patient_id=1,
#         doctor_id=2,
#         appointment_date=datetime.now() + timedelta(days=1),
#         reason='Annual checkup',
#         status='Scheduled'
#     )
#     appt2 = Appointment(
#         patient_id=2,
#         doctor_id=1,
#         appointment_date=datetime.now() + timedelta(days=2),
#         reason='Follow-up on blood test',
#         status='Scheduled'
#     )
#     db.session.add(appt1)
#     db.session.add(appt2)
    
#     # Create admissions
#     admission1 = Admission(
#         patient_id=1,
#         admission_date=datetime.now() - timedelta(days=3),
#         room_number='101',
#         bed_number='A',
#         diagnosis='Pneumonia',
#         status='Admitted'
#     )
#     db.session.add(admission1)
    
#     # Create test results
#     test1 = TestResult(
#         patient_id=2,
#         test_name='Complete Blood Count',
#         test_date=datetime.now() - timedelta(days=7),
#         result='All values within normal range',
#         doctor_id=1
#     )
#     db.session.add(test1)
    
#     # Create staff schedules
#     schedule1 = StaffSchedule(
#         staff_id=4,  # nurse_amy
#         shift_start=datetime.now().replace(hour=8, minute=0, second=0),
#         shift_end=datetime.now().replace(hour=20, minute=0, second=0),
#         department='Emergency'
#     )
#     schedule2 = StaffSchedule(
#         staff_id=5,  # staff_mike
#         shift_start=datetime.now().replace(hour=9, minute=0, second=0),
#         shift_end=datetime.now().replace(hour=17, minute=0, second=0),
#         department='Administration'
#     )
#     db.session.add(schedule1)
#     db.session.add(schedule2)
    
#     # Create attendance records
#     attendance1 = Attendance(
#         staff_id=4,
#         date=datetime.now().date(),
#         check_in=datetime.now().replace(hour=8, minute=5, second=0),
#         status='Present'
#     )
#     attendance2 = Attendance(
#         staff_id=5,
#         date=datetime.now().date(),
#         check_in=datetime.now().replace(hour=9, minute=15, second=0),
#         status='Late'
#     )
#     db.session.add(attendance1)
#     db.session.add(attendance2)
    
#     # Create billing records
#     bill1 = Billing(
#         patient_id=1,
#         admission_id=1,
#         amount=1250.50,
#         date_issued=datetime.now(),
#         due_date=datetime.now() + timedelta(days=30),
#         status='Pending',
#         insurance_claim=True,
#         insurance_provider='Blue Cross',
#         claim_status='Submitted'
#     )
#     bill2 = Billing(
#         patient_id=2,
#         amount=350.75,
#         date_issued=datetime.now(),
#         due_date=datetime.now() + timedelta(days=30),
#         status='Paid'
#     )
#     db.session.add(bill1)
#     db.session.add(bill2)
    
#     # Commit all changes
#     db.session.commit()

# if __name__ == '__main__':
#     with app.app_context():
#         create_sample_data()
#     print("Sample data created successfully!")