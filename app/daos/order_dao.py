from app.models import LogType
from app.models.order import Order, OrderStatus, OrderDetails, OfflineOrder, OnlineOrder, OrderLog, ORDER_STATUS_MAP, Regulation
from flask_login import current_user
from app.extensions import db
from sqlalchemy.sql import extract
from sqlalchemy import func, cast, Date


def load_orders(order_type, order_status):
    query = Order.query

    if order_type:
        query = query.filter(Order.order_type.__eq__(order_type))

    if order_status != 'ALL':
        query = query.filter(Order.status.__eq__(order_status))

    return query.all()

def get_order_by_id(id):
    return Order.query.filter_by(id=id).first()

def get_online_order_by_id(id, customer_id):
    return OnlineOrder.query.filter_by(id=id, customer_id=customer_id).first()

def add_offline_order(draft, note, table):
    if not draft:
        raise ValueError("Draft is empty")

    try:
        order = OfflineOrder(
            status=OrderStatus.CONFIRMED,
            note=note,
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

def get_online_order_by_status(status, customer_id):
    return OnlineOrder.query.filter_by(customer_id=customer_id, status=status).first()

def get_offline_order_by_id(id):
    return OfflineOrder.query.get(id)

def update_online_order(cart, customer_id, address, note):
    if not cart:
        raise ValueError("Giỏ hàng trống")

    order = get_online_order_by_status(status=OrderStatus.UNPAID, customer_id=customer_id)
    #phát triển thêm ràng buộc 1 Kh có nhiều order pending nhưng chỉ có 1 order pending trong trạng thái chưa thanh toán

    try:
        if order:
            order.customer_address = address
            order.note = note

            for d in order.details:
                db.session.delete(d)
        else:
            order = OnlineOrder(
                customer_id=customer_id,
                customer_address=address,
                status=OrderStatus.UNPAID,
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
        return order.id

    except Exception as e:
        db.session.rollback()
        print("Lỗi Sync Order:", e)
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
    r = Regulation.query.filter(Regulation.key.__eq__(key)).first()
    return r.value

def count_order_by_time(from_date=None, to_date=None):
    query = db.session.query(func.count(Order.id))

    if from_date:
        query = query.filter(Order.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(cast(Order.created_date, Date).__le__(to_date))

    return query.scalar()

def revenue_by_day(from_date=None, to_date=None):
    query = db.session.query(func.sum(OrderDetails.quantity * OrderDetails.unit_price))\
                      .join(Order, OrderDetails.order_id.__eq__(Order.id))

    if from_date:
        query = query.filter(Order.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(cast(Order.created_date, Date).__le__(to_date))

    return query.scalar()

def revenue_month_stats(year):
    return db.session.query(extract('month', Order.created_date), func.sum(OrderDetails.quantity * OrderDetails.unit_price))\
                     .join(Order, Order.id.__eq__(OrderDetails.order_id))\
                     .filter(extract('year', Order.created_date) == year)\
                     .group_by(extract('month', Order.created_date))\
                     .order_by(extract('month', Order.created_date)).all()