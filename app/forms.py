import re

from wtforms.fields.choices import SelectField
from wtforms.validators import ValidationError, InputRequired, length, DataRequired, EqualTo, Email, Optional

from app.models.user import User, Employee, Waiter, Manager, Cashier, Gender
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, HiddenField


def unique_email(form, field):
    query = User.query.filter(User.email == field.data)

    user_id_field = getattr(form, "user_id", None)
    if user_id_field is not None and user_id_field.data:
        query = query.filter(User.id != user_id_field.data)

    if query.first():
        raise ValidationError('Email already exists.')

def unique_identity_card(form, field):
    if Employee.query.filter(Employee.identity_card == field.data, Employee.id != form.user_id.data).first():
        raise ValidationError('Identity Card already exists.')

def unique_phone(form, field):
    query = User.query.filter(User.phone == field.data)
    user_id_field = getattr(form, "user_id", None)
    if user_id_field is not None and user_id_field.data:
        query = query.filter(User.id != user_id_field.data)
    if query.first():
        raise ValidationError('Phone already exists.')

def unique_username(form, field):
    query = User.query.filter(User.username == field.data)

    # nếu form có user_id (form edit), loại trừ chính user đó
    user_id_field = getattr(form, "user_id", None)
    if user_id_field is not None and user_id_field.data:
        query = query.filter(User.id != user_id_field.data)

    if query.first():
        raise ValidationError('Username already exists.')

def unique_driver_license(form, field):
    if Waiter.query.filter(Waiter.driver_license == field.data, Waiter.id != form.user_id.data).first():
        raise ValidationError('Driver license already exists.')

def unique_graduation_certificate(form, field):
    if Manager.query.filter_by(Manager.graduation_certificate == field.data, User.id != form.user_id.data).first():
        raise ValidationError('Graduation certificate already exists.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    fullname = StringField('Fullname', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired(), length(min=4, max=20), unique_username])
    phone = StringField('Phone', validators=[InputRequired(), length(min=10, max=10), unique_phone])
    password = PasswordField('Password', validators=[InputRequired(), length(min=4, max=20)])
    confirm = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

class CustomerRegisterForm(RegisterForm):
    pass

class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    submit = SubmitField('Reset Password')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match.')])
    submit = SubmitField('Change Password')

    def validate_new_password(self, field):
        password = field.data
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one digit.')
        if not re.search(r'[\W_]', password):
            raise ValidationError('Password must contain at least one special character.')

class EmployeeRegisterForm(RegisterForm):
    email = StringField('Email', validators=[InputRequired(), unique_email])
    dob = DateField('Date of Birth', validators=[DataRequired()], format="%Y-%m-%d")
    avatar = StringField('Avatar')
    gender = StringField('Gender')
    address = StringField('Address')
    identity_card = StringField('Identity Card', validators=[InputRequired(), unique_identity_card])

class WaiterRegisterForm(EmployeeRegisterForm):
    driver_license = StringField('Driver License', validators=[InputRequired(), unique_driver_license])

class ManagerRegisterForm(EmployeeRegisterForm):
    graduation_certificates = StringField('Graduation Certificate', validators=[InputRequired(), unique_graduation_certificate])

class EditForm(FlaskForm):
    user_id = HiddenField()
    fullname = StringField('Fullname', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), unique_phone])
    dob = DateField('Date of Birth', validators=[Optional()], format="%Y-%m-%d")
    email = StringField('Email', validators=[Optional(), Email(), unique_email])
    gender = SelectField('Gender', choices=[('', 'Chọn giới tính')] + [(g.name, g.value) for g in Gender],
        validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    submit = SubmitField('Save')

class CustomerEditForm(EditForm):
    pass

class ChangeAvatarForm(FlaskForm):
    avatar = StringField('Avatar', validators=[DataRequired()])
    submit = SubmitField('Save')

class EmployeeEditForm(EditForm):
    identity_card = StringField('Identity Card', validators=[DataRequired(), unique_identity_card])
    submit = SubmitField('Save')

class WaiterEditForm(EmployeeEditForm):
    driver_license = StringField('Driver license', validators=[DataRequired(), unique_driver_license])