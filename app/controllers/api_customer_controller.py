from flask import Blueprint, jsonify, request, session
from flask_login import login_required

from app.decorators import customer_required
from app.utils import get_total_session
from app.daos.dish_dao import get_dish_by_id
from app.daos.order_dao import add_online_order


api_customer = Blueprint('api_customer', __name__)

@api_customer.route('/cart/add', methods=['post'])
@login_required
@customer_required
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

    return jsonify(get_total_session(cart=cart))

@api_customer.route('/pay', methods=['post'])
@login_required
@customer_required
def pay():
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