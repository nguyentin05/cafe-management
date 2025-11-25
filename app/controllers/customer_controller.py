from flask import render_template, Blueprint
from flask_login import login_required

from app.decorators import customer_required

customer = Blueprint('customer', __name__)

@customer.route('/info')
@login_required
@customer_required
def info():
    return render_template('customer/info.html')

@customer.route('/cart', methods=['get', 'post'])
@login_required
@customer_required
def cart():
    return render_template('customer/cart.html')

@customer.route("/orders/<int:id>")
@login_required
@customer_required
def order_detail(id):
    return render_template("customer/order_detail.html")