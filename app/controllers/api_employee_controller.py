from flask import Blueprint, jsonify, request, session
from flask_login import login_required, current_user

from app import redis_client
from app.utils import get_total_session
from app.daos.order_dao import add_offline_order, get_order_by_id, update_offline_order, next_order_status, \
    cancel_order_status, get_value
from app.decorators import waiter_required, employee_required, manager_required
from app.models.order import OrderType, OrderStatus
from app.daos.dish_dao import count_dishes
from app.daos.inventory_dao import add_note, add_report
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

    total_tats = get_total_session(cart=draft)
    total_quantity = total_tats['total_quantity']

    limit = int(get_value('MAX_QUANTITY'))

    if total_quantity > limit:
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


@api_employee.route('/orders/update/<int:id>', methods=['put'])
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

    if total_quantity > 10:
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


@api_employee.route('/orders/next/<int:id>', methods=['put'])
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


@api_employee.route('/orders/cancel/<int:id>', methods=['put'])
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
    cost = data.get('cost')
    quantity = float(data.get('quantity'))

    today = date.today().isoformat()
    key = f'inventory_report:{today}:{current_user.id}'

    report = redis_client.hget(key, id)

    if report:
        obj = json.loads(report)
        obj['quantity'] = quantity
        obj['cost'] = cost
        obj['name'] = name
    else:
        obj = {
            'id': int(id),
            'name': name,
            'cost': cost,
            'quantity': quantity
        }

    redis_client.hset(key, id, json.dumps(obj))

    return jsonify({'code': 200})

@api_employee.route('/report-inventory/delete/<id>', methods=['delete'])
@login_required
@waiter_required
def delete_from_report(id):
    today = date.today().isoformat()
    key = f'inventory_report:{today}:{current_user.id}'

    redis_client.hdel(key, str(id))

    return jsonify({'code': 200})
