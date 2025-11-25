from app.models.order import Order, OrderStatus, OrderDetails, OfflineOrder, OnlineOrder
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
            waiter_id=int(current_user.id),
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

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print('ERROR in add_offline_order:', e)
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