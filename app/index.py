from flask import render_template, request, redirect, url_for
from app import app, login
from app.dao import *
from flask_login import login_user, logout_user

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods = ['get', 'post'])
def user_register():
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
                return redirect(url_for('user_signin'))
            else:
                err_msg = 'Mat khau khong khop'
        except Exception as ex:
            err_msg = 'He thong loi' + str(ex)

    return render_template('register.html', err_msg=err_msg)

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg = 'username hoac password ko chinh xac'

    return render_template('login.html', err_msg=err_msg)

@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))

@login.user_loader
def user_load(user_id):
    return get_user_by_id(user_id)

@app.route('/menu')
def menu():
    dish_cate = request.args.get('dishCate')
    dishes = load_dishes(dish_cate)
    return render_template('menu.html', dishes=dishes)

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/menu/<int:id>')
def detailMenu(id):
    pass

@app.context_processor
def common_response():
    return {
        'dish_categories': load_dish_categories()
    }

if __name__ == '__main__':
    with app.app_context():
        from app.admin import *
        app.run(debug=True)