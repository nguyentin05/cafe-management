from app.models import LogType
from app.models.order import Order, OrderStatus, OrderDetails, OfflineOrder, OnlineOrder, OrderLog, ORDER_STATUS_MAP, Regulation
from flask_login import current_user
from app.extensions import db

def load_orders(order_type, order_status):
    query = Order.query

    if order_type:
        query = query.filter(Order.order_type.__eq__(order_type))

    if order_status != 'ALL':
        query = query.filter(Order.status.__eq__(order_status))

    return query.all()

def get_order_by_id(id):
    return Order.query.get(id)

def add_offline_order(draft, note, table):
    if not draft:
        raise ValueError("Draft is empty")

    try:
        order = OfflineOrder(
            status=OrderStatus.CONFIRMED,
            note=note,
            waiter_id=current_user.id,
            table_number=int(table)
        )
        db.session.add(order)
        db.session.flush()

        for c in draft.values():
            d = OrderDetails(
                order_id=order.id,
                dish_id=c['id'],
                quantity=c['quantity'],
                unit_price=c['price']
            )
            db.session.add(d)

        add_log(order_id=order.id, action_type=LogType.CREATED)

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print('ERROR in add_offline_order:', e)
        raise e

def update_offline_order(order, items, note, table):
    try:
        order.note = note
        order.table_number = table

        for detail in order.details:
            db.session.delete(detail)

        for item in items:
            order_detail = OrderDetails(
                order_id=order.id,
                dish_id=item['id'],
                quantity=int(item['quantity']),
                unit_price=item['price']
            )
            db.session.add(order_detail)

        add_log(order_id=order.id, action_type=LogType.EDITED)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print('ERROR in update_order:', e)
        raise e

def add_online_order(cart, address, note):
    if not cart:
        raise ValueError("Cart is empty")

    try:
        order = OnlineOrder(
            customer_id=current_user.id,
            customer_address=address,
            status=OrderStatus.PENDING,
            note=note
        )
        db.session.add(order)
        db.session.flush()

        for c in cart.values():
            d = OrderDetails(
                order_id=order.id,
                dish_id=c['id'],
                quantity=c['quantity'],
                unit_price=c['price']
            )
            db.session.add(d)

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print('ERROR in add_online_order:', e)
        raise e

def get_total_order(id):
    total_quantity, total_amount = 0, 0

    order = get_order_by_id(id=id)

    for c in order.details:
        total_quantity += c.quantity
        total_amount += c.quantity * c.unit_price

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }

def add_log(order_id, action_type, form_status=None, to_status=None):
    user_id = current_user.id
    if action_type == LogType.CHANGED_STATUS:
        description = f'{user_id} {action_type.value} order#{order_id} from {form_status} to {to_status}'
    else:
        description = f'{user_id} {action_type.value} order#{order_id}'

    try:
        log = OrderLog(order_id=order_id,
                       action_type=action_type,
                       from_status=form_status,
                       to_status=to_status,
                       description=description,
                       employee_id=user_id)
        db.session.add(log)

    except Exception as e:
        db.session.rollback()
        print('ERROR in add_log:', e)
        raise e

def next_order_status(order):
    flow = ORDER_STATUS_MAP.get(order.order_type)

    try:
        status = flow.index(order.status)

        from_status = order.status

        if status + 1 < len(flow) - 1:
            next_status = flow[status + 1]

            order.status = next_status

            add_log(order_id=order.id, action_type=LogType.CHANGED_STATUS, form_status=from_status, to_status=order.status)

            db.session.commit()

    except Exception as e:
        db.session.rollback()
        print('ERROR in change_order_status:', e)
        raise e

def cancel_order_status(order):
    try:
        order.status = OrderStatus.CANCELED

        add_log(order_id=order.id, action_type=LogType.CANCELED)

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print('ERROR in cancel_order:', e)
        raise e

def get_value(key):
    r = Regulation.query.filter(Regulation.key == key).first()
    return r.value