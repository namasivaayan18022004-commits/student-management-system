from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, TextAreaField, DateField, FloatField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from models import Student, Teacher, Mark

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class StudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired(), Length(min=2, max=50)])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=150)])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    department = SelectField('Department', choices=[
        ('Computer Science', 'Computer Science'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Business Administration', 'Business Administration'),
        ('Arts & Humanities', 'Arts & Humanities')
    ], validators=[DataRequired()])
    year = SelectField('Year', choices=[
        ('First Year', 'First Year'),
        ('Second Year', 'Second Year'),
        ('Third Year', 'Third Year'),
        ('Fourth Year', 'Fourth Year')
    ], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    address = TextAreaField('Address', validators=[DataRequired()])
    photo = FileField('Student Photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    status = SelectField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')], validators=[DataRequired()])
    submit = SubmitField('Save Student')

    def validate_student_id(self, student_id):
        # We only validate unique on create if we can, but since this form is used for update too,
        # we will handle uniqueness logic in the route.
        pass

class TeacherForm(FlaskForm):
    teacher_id = StringField('Teacher ID', validators=[DataRequired(), Length(min=2, max=50)])
    employee_id = StringField('Employee ID', validators=[DataRequired(), Length(min=2, max=50)])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=150)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    department = SelectField('Department', choices=[
        ('Computer Science', 'Computer Science'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Business Administration', 'Business Administration'),
        ('Arts & Humanities', 'Arts & Humanities'),
        ('Mathematics', 'Mathematics'),
        ('Physics', 'Physics')
    ], validators=[DataRequired()])
    designation = StringField('Designation', validators=[DataRequired(), Length(min=2, max=100)])
    qualification = StringField('Qualification', validators=[DataRequired(), Length(min=2, max=150)])
    experience = IntegerField('Experience (Years)', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    address = TextAreaField('Address', validators=[DataRequired()])
    joining_date = DateField('Joining Date', format='%Y-%m-%d', validators=[DataRequired()])
    salary = FloatField('Salary', validators=[DataRequired()])
    status = SelectField('Employment Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('On Leave', 'On Leave')], validators=[DataRequired()])
    photo = FileField('Profile Photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Save Teacher')

class MarkForm(FlaskForm):
    student_id = SelectField('Select Student', coerce=int, validators=[DataRequired()])
    department = SelectField('Department', choices=[
        ('Computer Science', 'Computer Science'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Business Administration', 'Business Administration'),
        ('Arts & Humanities', 'Arts & Humanities')
    ], validators=[DataRequired()])
    year = SelectField('Year', choices=[
        ('First Year', 'First Year'),
        ('Second Year', 'Second Year'),
        ('Third Year', 'Third Year'),
        ('Fourth Year', 'Fourth Year')
    ], validators=[DataRequired()])
    semester = SelectField('Semester', choices=[
        ('Sem 1', 'Semester 1'),
        ('Sem 2', 'Semester 2'),
        ('Sem 3', 'Semester 3'),
        ('Sem 4', 'Semester 4'),
        ('Sem 5', 'Semester 5'),
        ('Sem 6', 'Semester 6'),
        ('Sem 7', 'Semester 7'),
        ('Sem 8', 'Semester 8')
    ], validators=[DataRequired()])
    subject = StringField('Subject Name', validators=[DataRequired(), Length(min=2, max=150)])
    subject_code = StringField('Subject Code', validators=[DataRequired(), Length(min=2, max=50)])
    teacher = SelectField('Teacher', validators=[DataRequired()])
    internal_marks = FloatField('Internal Marks (Max 25)', default=0.0, validators=[DataRequired()])
    assignment_marks = FloatField('Assignment Marks (Max 10)', default=0.0, validators=[DataRequired()])
    practical_marks = FloatField('Practical Marks (Max 15)', default=0.0, validators=[DataRequired()])
    external_marks = FloatField('External Marks (Max 50)', default=0.0, validators=[DataRequired()])
    remarks = StringField('Remarks / Notes', validators=[Length(max=200)])
    submit = SubmitField('Save Marks')

class AttendanceForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    teacher_id = SelectField('Teacher (Marked By)', coerce=int, validators=[DataRequired()])
    date = StringField('Attendance Date (YYYY-MM-DD)', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave')
    ], validators=[DataRequired()])
    check_in_time = StringField('Check-In Time', default='09:00 AM', validators=[Length(max=20)])
    check_out_time = StringField('Check-Out Time', default='04:30 PM', validators=[Length(max=20)])
    remarks = StringField('Remarks / Notes', validators=[Length(max=200)])
    submit = SubmitField('Save Attendance')

class FeeForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    fee_category = SelectField('Fee Category', choices=[
        ('Admission Fee', 'Admission Fee'),
        ('Tuition Fee', 'Tuition Fee'),
        ('Examination Fee', 'Examination Fee'),
        ('Laboratory Fee', 'Laboratory Fee'),
        ('Library Fee', 'Library Fee'),
        ('Sports Fee', 'Sports Fee'),
        ('Hostel Fee', 'Hostel Fee'),
        ('Transport Fee', 'Transport Fee'),
        ('Miscellaneous Fee', 'Miscellaneous Fee'),
        ('Custom', 'Custom Category...')
    ], validators=[DataRequired()])
    custom_category = StringField('Custom Fee Category Name', validators=[Length(max=100)])
    academic_year = SelectField('Academic Year', choices=[
        ('2023-2024', '2023-2024'),
        ('2024-2025', '2024-2025'),
        ('2025-2026', '2025-2026'),
        ('2026-2027', '2026-2027')
    ], validators=[DataRequired()])
    semester = SelectField('Semester', choices=[
        ('Sem 1', 'Semester 1'),
        ('Sem 2', 'Semester 2'),
        ('Sem 3', 'Semester 3'),
        ('Sem 4', 'Semester 4'),
        ('Sem 5', 'Semester 5'),
        ('Sem 6', 'Semester 6'),
        ('Sem 7', 'Semester 7'),
        ('Sem 8', 'Semester 8')
    ], validators=[DataRequired()])
    total_fee = FloatField('Total Fee Amount (₹)', default=0.0, validators=[DataRequired()])
    scholarship_discount = FloatField('Scholarship / Discount (₹)', default=0.0)
    fine_amount = FloatField('Fine Amount (₹)', default=0.0)
    amount_paid = FloatField('Amount Paid (₹)', default=0.0)
    payment_method = SelectField('Payment Method', choices=[
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Debit Card', 'Debit Card'),
        ('Credit Card', 'Credit Card'),
        ('Net Banking', 'Net Banking'),
        ('Cheque', 'Cheque')
    ], validators=[DataRequired()])
    transaction_reference = StringField('Transaction Reference / UTR / Cheque No.', validators=[Length(max=100)])
    payment_date = StringField('Payment Date (YYYY-MM-DD)', validators=[Length(max=20)])
    due_date = StringField('Due Date (YYYY-MM-DD)', validators=[DataRequired(), Length(max=20)])
    remarks = StringField('Remarks / Notes', validators=[Length(max=200)])
    submit = SubmitField('Save Fee Record')

