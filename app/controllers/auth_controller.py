from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from app.daos.user_dao import add_customer, auth_user, get_user_by_id
from app import login
from app.forms import LoginForm, CustomerRegisterForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods = ['get', 'post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.menu'))

    form = CustomerRegisterForm()
    err_msg = ''

    if form.validate_on_submit():
        fullname = form.fullname.data
        username = form.username.data
        password = form.password.data
        phone = form.phone.data

        try:
            add_customer(fullname=fullname, username=username, password=password, phone=phone)
            return redirect(url_for('auth.signin'))
        except Exception as ex:
            err_msg = 'He thong loi ' + str(ex)

    return render_template('auth/register.html', form=form, err_msg=err_msg)

@auth.route('/login', methods=['get', 'post'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.menu'))

    form = LoginForm()
    err_msg = ''

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = auth_user(username=username, password=password)

        if user:
            login_user(user=user)

            next = request.args.get('next', 'main.menu')

            if current_user.is_admin:
                return redirect('/admin')

            if current_user.is_employee:
                return redirect(url_for('employee_web.dashboard'))

            return redirect(url_for(next))
        else:
            err_msg = 'username hoac password ko chinh xac'

    return render_template('auth/login.html', form=form, err_msg=err_msg)


@auth.route('/logout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('auth.signin'))

@login.user_loader
def user_load(user_id):
    return get_user_by_id(user_id)