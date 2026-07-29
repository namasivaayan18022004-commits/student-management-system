from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    full_name = db.Column(db.String(150), nullable=True, default='System Administrator')
    email = db.Column(db.String(150), nullable=True, default='admin@college.edu')
    phone = db.Column(db.String(50), nullable=True, default='9840123456')
    address = db.Column(db.Text, nullable=True, default='1, Administration Block, College Campus, Pondicherry')
    photo = db.Column(db.String(200), nullable=True, default='default_admin.png')
    role = db.Column(db.String(50), nullable=False, default='Super Admin')
    status = db.Column(db.String(20), nullable=False, default='Active')
    last_login = db.Column(db.DateTime, nullable=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(200), nullable=True) # store filename
    status = db.Column(db.String(20), nullable=False, default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    marks = db.relationship('Mark', backref='student_ref', lazy=True, cascade='all, delete-orphan')
    attendance_records = db.relationship('Attendance', backref='student_ref', lazy=True, cascade='all, delete-orphan')
    fee_records = db.relationship('Fee', backref='student_ref', lazy=True, cascade='all, delete-orphan')

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String(50), unique=True, nullable=False)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(150), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text, nullable=False)
    joining_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Active')
    photo = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    marked_attendance = db.relationship('Attendance', backref='teacher_ref', lazy=True)

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    student_name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    subject_code = db.Column(db.String(50), nullable=False)
    teacher = db.Column(db.String(150), nullable=False)
    internal_marks = db.Column(db.Float, nullable=False, default=0.0)
    assignment_marks = db.Column(db.Float, nullable=False, default=0.0)
    practical_marks = db.Column(db.Float, nullable=False, default=0.0)
    external_marks = db.Column(db.Float, nullable=False, default=0.0)
    total_marks = db.Column(db.Float, nullable=False, default=0.0)
    percentage = db.Column(db.Float, nullable=False, default=0.0)
    grade = db.Column(db.String(10), nullable=False)
    grade_point = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String(10), nullable=False)
    remarks = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Attendance(db.Model):
    __table_args__ = (db.UniqueConstraint('student_id', 'date', name='uq_student_date'),)
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    student_name = db.Column(db.String(150), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=True)
    teacher_name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(20), nullable=False, index=True)
    day = db.Column(db.String(20), nullable=False)
    academic_year = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Present')
    check_in_time = db.Column(db.String(20), nullable=True, default='09:00 AM')
    check_out_time = db.Column(db.String(20), nullable=True, default='04:30 PM')
    remarks = db.Column(db.String(200), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Fee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    student_name = db.Column(db.String(150), nullable=False)
    fee_category = db.Column(db.String(100), nullable=False)
    academic_year = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    total_fee = db.Column(db.Float, nullable=False, default=0.0)
    scholarship_discount = db.Column(db.Float, nullable=False, default=0.0)
    fine_amount = db.Column(db.Float, nullable=False, default=0.0)
    amount_paid = db.Column(db.Float, nullable=False, default=0.0)
    remaining_balance = db.Column(db.Float, nullable=False, default=0.0)
    payment_status = db.Column(db.String(30), nullable=False, default='Pending')
    payment_method = db.Column(db.String(50), nullable=True, default='Cash')
    transaction_reference = db.Column(db.String(100), nullable=True)
    payment_date = db.Column(db.String(20), nullable=True)
    due_date = db.Column(db.String(20), nullable=False)
    collected_by = db.Column(db.String(150), nullable=False, default='Admin')
    remarks = db.Column(db.String(200), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ReportHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_name = db.Column(db.String(200), nullable=False)
    report_type = db.Column(db.String(100), nullable=False)
    generated_by = db.Column(db.String(150), nullable=False, default='Admin')
    generated_on = db.Column(db.DateTime, default=datetime.utcnow)
    parameters = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), nullable=False, default='Generated')
    downloads = db.Column(db.Integer, nullable=False, default=0)

class ReportTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(150), nullable=False)
    report_type = db.Column(db.String(100), nullable=False)
    date_range_type = db.Column(db.String(50), nullable=True)
    parameters_json = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.String(150), nullable=False, default='Admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CollegeSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    college_name = db.Column(db.String(200), nullable=False, default="Pondicherry Engineering College")
    college_logo = db.Column(db.String(200), nullable=True, default="default_logo.png")
    college_address = db.Column(db.Text, nullable=False, default="Pillaichavadi, East Coast Road")
    city = db.Column(db.String(100), nullable=False, default="Pondicherry")
    state = db.Column(db.String(100), nullable=False, default="Puducherry")
    country = db.Column(db.String(100), nullable=False, default="India")
    postal_code = db.Column(db.String(20), nullable=False, default="605014")
    phone_number = db.Column(db.String(50), nullable=False, default="+91-413-2655281")
    email_address = db.Column(db.String(150), nullable=False, default="info@pec.edu")
    website_url = db.Column(db.String(150), nullable=False, default="https://www.pec.edu")
    academic_year = db.Column(db.String(50), nullable=False, default="2025-2026")
    college_description = db.Column(db.Text, nullable=True, default="A premier technical institute committed to academic excellence and research innovation.")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SecuritySettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enable_2fa = db.Column(db.Boolean, nullable=False, default=False)
    auto_logout = db.Column(db.Boolean, nullable=False, default=True)
    max_login_attempts = db.Column(db.Integer, nullable=False, default=5)
    lock_duration_minutes = db.Column(db.Integer, nullable=False, default=30)
    password_policy_strong = db.Column(db.Boolean, nullable=False, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class NotificationSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_notifications = db.Column(db.Boolean, nullable=False, default=True)
    fee_reminders = db.Column(db.Boolean, nullable=False, default=True)
    attendance_alerts = db.Column(db.Boolean, nullable=False, default=True)
    marks_notifications = db.Column(db.Boolean, nullable=False, default=True)
    report_notifications = db.Column(db.Boolean, nullable=False, default=True)
    system_notifications = db.Column(db.Boolean, nullable=False, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EmailSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    smtp_server = db.Column(db.String(150), nullable=False, default="smtp.gmail.com")
    smtp_port = db.Column(db.Integer, nullable=False, default=587)
    email_address = db.Column(db.String(150), nullable=False, default="notifications@pec.edu")
    app_password = db.Column(db.String(150), nullable=True, default="")
    sender_name = db.Column(db.String(150), nullable=False, default="College ERP Notifier")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AppearanceSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme_mode = db.Column(db.String(50), nullable=False, default="light")
    sidebar_color = db.Column(db.String(50), nullable=False, default="#0d6efd")
    accent_color = db.Column(db.String(50), nullable=False, default="#0d6efd")
    font_size = db.Column(db.String(50), nullable=False, default="medium")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BackupHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    file_size = db.Column(db.String(50), nullable=False)
    backup_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(150), nullable=False, default="Admin")
    notes = db.Column(db.String(200), nullable=True, default="Manual Backup")


class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    admin_user = db.Column(db.String(150), nullable=False, default="Admin")
    action = db.Column(db.String(255), nullable=False)
    module = db.Column(db.String(100), nullable=False, default="System")
    ip_address = db.Column(db.String(50), nullable=True, default="127.0.0.1")


