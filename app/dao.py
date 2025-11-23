from flask_login import current_user
from app.utils import hash_password
from app import app, db
from app.models import DishCategory, Dish, User, UserRole, Customer, CategoryGroup, OfflineOrder, Order, OrderDetails, OnlineOrder, OrderStatus, OrderType
import hashlib

def load_category_groups():
    return CategoryGroup.query.all()

def load_dish_categories():
    return DishCategory.query.all()

def load_dishes(dish_cate=None):
    query = Dish.query

    if dish_cate:
        query = query.filter(Dish.dishCategory_id.__eq__(dish_cate))

    return query.all()

def get_dish_by_id(id):
    return Dish.query.get(id)

def get_dish_category_by_id(id):
    return DishCategory.query.get(id)

def load_orders(order_type, order_status):
    query = Order.query

    if order_type:
        query = query.filter(Order.order_type.__eq__(order_type))

    if order_status != 'ALL':
        query = query.filter(Order.status.__eq__(order_status))

    return query.all()

def add_customer(fullname, username, password, **kwargs):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    user = Customer(fullname = fullname.strip(),
                username = username.strip(),
                password = password,
                email = kwargs.get('email'))

    db.session.add(user)
    db.session.commit()

def check_login(username, password, role=None):
    password = hash_password(password)

    u = User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password))

    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()

def get_user_by_id(id):
    return User.query.get(id)

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

def add_online_order(cart, address):
    if not cart:
        raise ValueError("Cart is empty")

    try:
        order = OnlineOrder(
            customer_id=current_user.id,
            customer_address=address,
            status=OrderStatus.PENDING
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