from flask import Blueprint, jsonify, request, session, flash, redirect, url_for
from flask_login import login_required, current_user

from app import redis_client
from app.daos.payment_dao import MomoStrategy, process_order_payment
from app.utils import get_total_session
from app.daos.order_dao import add_offline_order, get_order_by_id, update_offline_order, next_order_status, \
    cancel_order_status, get_value, get_offline_order_by_id
from app.decorators import waiter_required, employee_required, manager_required, cashier_required
from app.models.order import OrderType, OrderStatus, RegulationKey
from app.daos.dish_dao import count_dishes
from app.daos.inventory_dao import add_note
from datetime import date
import json

api_employee = Blueprint('api_employee', __name__)


@api_employee.route('/complete', methods=['post'])
@login_required
@waiter_required
def complete():
    data = request.json
    table = data.get('table')
    note = data.get('note', '')
    draft = data.get('draft')

    total_stats = get_total_session(cart=draft)
    total_quantity = total_stats['total_quantity']

    MAX_QUANTITY = int(get_value('MAX_QUANTITY'))

    if total_quantity > MAX_QUANTITY:
        return jsonify({
            'code': 400,
            'message': 'qua so luong cho phep'
        })

    try:
        if not draft:
            return jsonify({'code': 400, 'message': 'Gio hang rong'})

        add_offline_order(draft, note=note, table=table)
    except Exception as ex:
        print(str(ex))
        return jsonify({'code': 400})

    return jsonify({'code': 200})


@api_employee.route('/orders/<int:id>/update', methods=['put'])
@login_required
@employee_required
def update_order(id):
    order = get_order_by_id(id=id)

    if not order.is_editable:
        return jsonify({'code': 400})

    data = request.json
    note = data.get('note', '')
    table = data.get('table')
    items = data.get('items')

    total_quantity = count_dishes(items)

    MAX_QUANTITY = get_value(key=RegulationKey.MAX_QUANTITY)

    if total_quantity > MAX_QUANTITY:
        return jsonify({
            'code': 400,
            'message': 'qua so luong cho phep'
        })

    if order.order_type.name == OrderType.OFFLINE and table is None:
        return jsonify({
            'code': 400,
            'message': 'chua co so ban'})

    try:
        update_offline_order(order=order, items=items, note=note, table=table)

    except Exception as ex:
        print(str(ex))
        return jsonify({'code': 400})

    return jsonify({'code': 200})


@api_employee.route('/orders/<int:id>/next', methods=['put'])
@login_required
@employee_required
def next_status(id):
    order = get_order_by_id(id=id)

    if order.status.name == OrderStatus.READY_TO_PAY:
        if not (current_user.is_cashier or current_user.is_manager):
            return jsonify({'code': 403})

    try:
        next_order_status(order=order)

    except Exception as ex:
        print(str(ex))
        return jsonify({'code': 400})

    return jsonify({'code': 200})


@api_employee.route('/orders/<int:id>/cancel', methods=['put'])
@login_required
@manager_required
def cancel_order(id):
    order = get_order_by_id(id=id)

    if not current_user.is_manager:
        return jsonify({'code': 403})

    if order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELED]:
        return jsonify({'code': 400, })

    try:
        cancel_order_status(order=order)
    except Exception as ex:
        print(str(ex))
        return jsonify({'code': 400})

    return jsonify({'code': 200})


@api_employee.route('/goods-receipt/add', methods=['post'])
@login_required
@waiter_required
def add_to_note():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    unit = data.get('unit')
    cost = data.get('cost')
    quantity = int(data.get('quantity'))
    note = session.get('note')

    if not note:
        note = {}

    if id in note:
        note[id]['quantity'] += quantity
    else:
        note[id] = {
            'id': id,
            'name': name,
            'cost': cost,
            'unit': unit,
            'quantity': quantity
        }

    session['note'] = note

    return jsonify({'code': 200})


@api_employee.route('/goods-receipt/delete/<id>', methods=['delete'])
@login_required
@waiter_required
def delete_from_note(id):
    note = session.get('note')

    if note and id in note:
        del note[id]
        session['note'] = note

    return jsonify({'code': 200})


@api_employee.route('/goods-receipt/save', methods=['post'])
@login_required
@waiter_required
def save_note():
    try:
        add_note(session.get('note'))
        session.pop('note', None)

    except Exception as ex:
        print(str(ex))
        return jsonify({'code': 400})

    return jsonify({'code': 200})


@api_employee.route('/report-inventory/add', methods=['post'])
@login_required
@waiter_required
def add_to_report():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    unit = data.get('unit')
    cost = data.get('cost')
    quantity = float(data.get('quantity'))

    today = date.today().isoformat()
    key = f'inventory_report:{today}:{current_user.id}'

    report = redis_client.hget(key, id)

    if report:
        obj = json.loads(report)
        obj['quantity'] = quantity
    else:
        obj = {
            'id': int(id),
            'name': name,
            'unit': unit,
            'cost': cost,
            'quantity': quantity
        }

    redis_client.hset(key, id, json.dumps(obj))

    return jsonify({'code': 200})


@api_employee.route('/report-inventory/<id>/delete', methods=['delete'])
@login_required
@waiter_required
def delete_from_report(id):
    today = date.today().isoformat()
    key = f'inventory_report:{today}:{current_user.id}'

    redis_client.hdel(key, str(id))

    return jsonify({'code': 200})


@api_employee.route('/orders/<int:order_id>/payment/create', methods=['get'])
@login_required
@cashier_required
def create_offline_payment(order_id):
    order = get_offline_order_by_id(order_id)

    if not order:
        flash("Đơn hàng không tồn tại", "danger")
        return redirect(url_for('employee_web.dashboard'))

    if order.status != OrderStatus.READY_TO_PAY:
        flash("Đơn hàng này ko thể thanh toán", "warning")
        return redirect(url_for('employee_web.dashboard'))

    strategy = MomoStrategy()

    try:
        payment = process_order_payment(order, strategy)

        if payment.pay_url:
            return redirect(payment.pay_url)

    except Exception as e:
        print(e)
        flash("Lỗi kết nối cổng thanh toán.", "danger")

    return redirect(url_for('employee_web.dashboard'))
