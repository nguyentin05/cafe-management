from flask import Blueprint, jsonify, request, session, current_app, flash, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.daos.payment_dao import PaymentStrategy, MomoStrategy, process_order_payment
from app.decorators import customer_required
from app.models import OnlineOrder, OrderStatus, MomoPayment
from app.utils import get_total_session, momo_sign
from app.daos.dish_dao import get_dish_by_id
from app.daos.order_dao import add_online_order, get_online_order_by_id

import requests
import uuid


api_customer = Blueprint('api_customer', __name__)

@api_customer.route('/cart/add', methods=['post'])
@login_required
@customer_required
def add_cart():
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

    return jsonify(get_total_session(cart=cart))

@api_customer.route('/pay', methods=['post'])
@login_required
@customer_required
def pay_cart():
    data = request.json
    address = data.get('address')
    orderNote = data.get('orderNote', '')

    try:
        add_online_order(session.get('cart'), address=address, note=orderNote)
        session.pop('cart', None)
    except Exception as ex:
        print(str(ex))
        return jsonify({'code': 400})

    return jsonify({'code': 200})


@api_customer.route('/cart/update/<dish_id>', methods=['put'])
@login_required
@customer_required
def update_cart(dish_id):
    cart = session.get('cart')

    if cart and dish_id in cart:
        cart[dish_id]['quantity'] += 1
        session['cart'] = cart

    return jsonify(get_total_session(cart=cart))

@api_customer.route('/cart/delete/<dish_id>', methods=['delete'])
@login_required
@customer_required
def delete_cart(dish_id):
    cart = session.get('cart')

    if cart and dish_id in cart:
        del cart[dish_id]
        session['cart'] = cart

    return jsonify(get_total_session(cart=cart))

@api_customer.route('/<order_id>/payment/create', methods=['GET'])
@login_required
@customer_required
def create_payment(order_id):
    order = get_online_order_by_id(id=order_id, customer_id=current_user.id)

    if not order:
        flash("Đơn hàng không ton tai", "danger")
        return redirect(url_for('main.menu'))

    if order.status != OrderStatus.UNPAID:
        flash("Đơn hàng da dc thanh toan", "danger")
        return redirect(url_for('customer.cart'))

    strategy = MomoStrategy()

    try:
        payment = process_order_payment(order, strategy)

        if payment.pay_url:
            return redirect(payment.pay_url)

    except Exception as e:
        print(e)
        flash("Lỗi kết nối cổng thanh toán.", "danger")
        return redirect(url_for('customer.checkout', order_id=order.id))

    return redirect(url_for('customer.checkout', order_id=order.id))