from flask import render_template, request, Blueprint
from flask_login import login_required

from app.daos.dish_dao import load_dishes
from app.decorators import employee_required, cashier_required
from app.models.order import OrderType, ORDER_STATUS_MAP
from app.daos.order_dao import load_orders, get_order_by_id, get_total_order

employee = Blueprint('employee_web', __name__)

@employee.route('/dashboard')
@login_required
@employee_required
def dashboard():
    order_type = (request.args.get('order_type', OrderType.OFFLINE.name)).upper()
    order_status = request.args.get('order_status', 'ALL')
    current_order_type = OrderType[order_type]
    orders = load_orders(order_type, order_status)
    return render_template('employee/dashboard.html',
                           current_order_status=order_status,
                           orders=orders,
                           order_types=list(OrderType),
                           current_order_type=current_order_type,
                           status_map=ORDER_STATUS_MAP)
@employee.route('/recipe')
@login_required
@employee_required
def recipe():
    return render_template('employee/comming-soon.html')


@employee.route('/cashier_shift')
@login_required
@cashier_required
def cashier_shift():
    return render_template('employee/comming-soon.html')

@employee.route('/dashboard/orders/<int:id>')
@login_required
@employee_required
def order_detail(id):
    total_order = get_total_order(id=id)
    order = get_order_by_id(id=id)
    return render_template('employee/order-detail.html', order=order, total_order=total_order)

@employee.route('/dashboard/orders/edit/<int:id>', methods=['get', 'post'])
@login_required
@employee_required
def edit_order(id):
    dishes = load_dishes()
    order = get_order_by_id(id=id)
    return render_template('employee/order-edit.html', order=order, dishes=dishes)