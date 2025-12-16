import re

from wtforms.fields.choices import SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import ValidationError, InputRequired, length, DataRequired, EqualTo, Email, Optional, Length

from app.models.user import User, Employee, Waiter, Manager, Cashier, Gender
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, HiddenField


def unique_email(form, field):
    query = User.query.filter(User.email == field.data)

    user_id_field = getattr(form, "user_id", None)
    if user_id_field is not None and user_id_field.data:
        query = query.filter(User.id != user_id_field.data)

    if query.first():
        raise ValidationError('Email đã tồn tại.')


def unique_identity_card(form, field):
    if Employee.query.filter(Employee.identity_card == field.data, Employee.id != form.user_id.data).first():
        raise ValidationError('Số căn cước công dân đã tồn tại.')


def unique_phone(form, field):
    query = User.query.filter(User.phone == field.data)
    user_id_field = getattr(form, "user_id", None)
    if user_id_field is not None and user_id_field.data:
        query = query.filter(User.id != user_id_field.data)
    if query.first():
        raise ValidationError('Số điện thoại đã tồn tại.')


def unique_username(form, field):
    query = User.query.filter(User.username == field.data)

    # nếu form có user_id (form edit), loại trừ chính user đó
    user_id_field = getattr(form, "user_id", None)
    if user_id_field is not None and user_id_field.data:
        query = query.filter(User.id != user_id_field.data)

    if query.first():
        raise ValidationError('Tài khoản đã tồn tại.')


def unique_driver_license(form, field):
    if Waiter.query.filter(Waiter.driver_license == field.data, Waiter.id != form.user_id.data).first():
        raise ValidationError('Số bằng lái xe đã tồn tại.')


def unique_graduation_certificate(form, field):
    if Manager.query.filter_by(Manager.graduation_certificate == field.data, User.id != form.user_id.data).first():
        raise ValidationError('Mã chứng nhận tốt nghiệp đã tồn tại.')


class LoginForm(FlaskForm):
    username = StringField('Tài khoản', validators=[InputRequired(), length(min=4, max=20)])
    password = PasswordField('Mật khẩu', validators=[InputRequired()])
    submit = SubmitField('Đăng nhập')


class RegisterForm(FlaskForm):
    fullname = StringField('Họ và tên', validators=[InputRequired()])
    username = StringField('Tài khoản', validators=[InputRequired(), length(min=4, max=20), unique_username])
    phone = StringField('Số điện thoại', validators=[InputRequired(), length(min=10, max=10), unique_phone])
    password = PasswordField('Mật khẩu', validators=[InputRequired(), length(min=4, max=20)])
    confirm = PasswordField('Xác nhận mật khẩu',
                            validators=[InputRequired(), EqualTo('password', message='Mật khẩu không khớp.')])
    submit = SubmitField('Đăng ký')


class CustomerRegisterForm(RegisterForm):
    pass

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Mật khẩu cũ', validators=[DataRequired()])
    new_password = PasswordField('Mật khẩu mới', validators=[DataRequired()])
    confirm_password = PasswordField('Xác nhận mật khẩu mới', validators=[DataRequired(), EqualTo('new_password',
                                                                                             message='Mật khẩu không khớp.')])
    submit = SubmitField('Đổi mật khẩu')

    def validate_new_password(self, field):
        password = field.data
        if len(password) < 8:
            raise ValidationError('Mật khẩu phải có ít nhất 8 ký tự.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Mật khẩu phải chứa ít nhất một chữ thường.')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Mật khẩu phải chứa ít nhất một chữ hoa.')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Mật khẩu phải chứa ít nhất một chữ số.')
        if not re.search(r'[\W_]', password):
            raise ValidationError('Mật khẩu phải chứa ít nhất một ký tự đặc biệt.')


class EmployeeRegisterForm(RegisterForm):
    email = StringField('Email', validators=[InputRequired(), unique_email])
    dob = DateField('Ngày sinh', validators=[DataRequired()], format="%Y-%m-%d")
    avatar = StringField('Ảnh đại diện')
    gender = StringField('Giới tính')
    address = StringField('Địa chỉ')
    identity_card = StringField('Căn cước công dân', validators=[InputRequired(), unique_identity_card])


class WaiterRegisterForm(EmployeeRegisterForm):
    driver_license = StringField('Bằng lái xe', validators=[InputRequired(), unique_driver_license])


class ManagerRegisterForm(EmployeeRegisterForm):
    graduation_certificates = StringField('Bằng tốt nghiệp',
                                          validators=[InputRequired(), unique_graduation_certificate])


class EditForm(FlaskForm):
    user_id = HiddenField()
    fullname = StringField('Họ và tên', validators=[DataRequired()])
    phone = StringField('Số điện thoại', validators=[DataRequired(), unique_phone])
    dob = DateField('Ngày sinh', validators=[Optional()], format="%Y-%m-%d")
    email = StringField('Email', validators=[Optional(), Email(), unique_email])
    # Phần choices giữ nguyên vì đã là tiếng Việt rồi
    gender = SelectField('Giới tính', choices=[('', 'Chọn giới tính')] + [(g.name, g.value) for g in Gender],
                         validators=[Optional()])
    address = StringField('Địa chỉ', validators=[Optional()])
    submit = SubmitField('Lưu thay đổi')


class CustomerEditForm(EditForm):
    pass


class ChangeAvatarForm(FlaskForm):
    avatar = StringField('Ảnh đại diện', validators=[DataRequired()])
    submit = SubmitField('Lưu ảnh')


class EmployeeEditForm(EditForm):
    identity_card = StringField('Căn cước công dân', validators=[DataRequired(), unique_identity_card])
    submit = SubmitField('Lưu thay đổi')


class WaiterEditForm(EmployeeEditForm):
    driver_license = StringField('Bằng lái xe', validators=[DataRequired(), unique_driver_license])


class OrderForm(FlaskForm):
    address = StringField('Địa chỉ nhận hàng', validators=[DataRequired(message="Vui lòng nhập địa chỉ nhận hàng.")])
    note = TextAreaField('Ghi chú đơn hàng', validators=[Length(max=200, message="Ghi chú không được quá 200 ký tự.")])
    submit = SubmitField('Thanh toán')