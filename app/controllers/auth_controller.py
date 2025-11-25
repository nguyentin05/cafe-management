from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from app.daos.user_dao import add_customer, check_login, get_user_by_id
from app import login

auth = Blueprint('auth', __name__)

@auth.route('/register', methods = ['get', 'post'])
def register():
    err_msg = ""

    if request.method.__eq__('POST'):
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')

        try:
            if password.strip().__eq__(confirm.strip()):
                add_customer(fullname=fullname, username=username, password=password, email=email)
                return redirect(url_for('auth.signin'))
            else:
                err_msg = 'Mat khau khong khop'
        except Exception as ex:
            err_msg = 'He thong loi' + str(ex)

    return render_template('auth/register.html', err_msg=err_msg)

@auth.route('/login', methods=['get', 'post'])
def signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('main.menu'))
        else:
            err_msg = 'username hoac password ko chinh xac'

    return render_template('auth/login.html', err_msg=err_msg)


@auth.route('/logout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('auth.signin'))

@login.user_loader
def user_load(user_id):
    return get_user_by_id(user_id)