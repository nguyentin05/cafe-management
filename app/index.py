from flask import render_template, request, redirect, url_for, session, jsonify
from app import app, login, utils, db
from app.dao import *
from flask_login import login_user, logout_user, login_required
from app.models import ORDER_STATUS_MAP

@app.route('/')
def home():
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
            return redirect(url_for('main'))
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
    current_cate = get_dish_category_by_id(dish_cate) if dish_cate else None
    dishes = load_dishes(dish_cate)
    return render_template('menu.html', dishes=dishes, current_cate=current_cate)

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/waiter/dashboard', methods=['get'])
def waiter_dashboard():
    order_type = (request.args.get('order_type', OrderType.OFFLINE.name)).upper()
    order_status = request.args.get('order_status', 'ALL')
    current_order_type = OrderType[order_type]

    orders = load_orders(order_type, order_status)

    return render_template('waiter/dashboard.html',
                           current_order_status=order_status,
                           orders=orders,
                           order_types=list(OrderType),
                           current_order_type=current_order_type,
                           status_map=ORDER_STATUS_MAP)

@app.route('/menu/<int:id>')
def detailMenu(id):
    pass

@app.route('/waiter/goods-receipt-note')
def goods_receipt_note():
    return render_template('waiter/goods-receipt-note.html')

@app.route('/waiter/offline-order')
def offline_order():
    return render_template('waiter/offline-order.html')

@app.route('/cart', methods=['get', 'post'])
def cart():
    if request.method.__eq__('POST'):
        address = request.form.get('address')

    return render_template('cart.html')

@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')
    cart = session.get('cart')

    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] +=1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'image': get_dish_by_id(id).image,
            'quantity': 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart=cart))

@app.route('/api/update-cart/<dish_id>', methods=['put'])
def update_cart(dish_id):
    cart = session.get('cart')

    if cart and dish_id in cart:
        cart[dish_id]['quantity'] += 1
        session['cart'] = cart

    return jsonify(utils.count_cart(cart=cart))

@app.route('/api/delete-cart/<dish_id>', methods=['delete'])
def delete_cart(dish_id):
    cart = session.get('cart')

    if cart and dish_id in cart:
        del cart[dish_id]
        session['cart'] = cart

    return jsonify(utils.count_cart(cart=cart))


@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    data = request.json
    address = data.get('address')
    try:
        add_online_order(session.get('cart'),address=address)
        del session['cart']
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})

@app.context_processor
def common_response():
    return {
        'dish_categories': load_dish_categories(),
        'category_groups': load_category_groups(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }