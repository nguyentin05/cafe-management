from flask_login import current_user

from app import app, db
from models import DishCategory, Dish, User, UserRole, Customer, CategoryGroup, Order, OrderDetails, OnlineOrder, OrderStatus
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

def add_customer(fullname, username, password, **kwargs):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    user = Customer(fullname = fullname.strip(),
                username = username.strip(),
                password = password,
                user_role = UserRole.CUSTOMER,
                email = kwargs.get('email'))

    db.session.add(user)
    db.session.commit()

def check_login(username, password, role=None):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()

    u = User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password))

    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()

def get_user_by_id(id):
    return User.query.get(id)

def add_online_order(cart):
    if cart:
        order = OnlineOrder(customer=current_user,
                            status=OrderStatus.PENDING,
                            )
        db.session.add(order)

        for c in cart.values():
            d = OrderDetails(order=order,
                             dish_id=c['id'],
                             quantity=c['quantity'],
                             unit_price=c['price'])
            db.session.add(d)

        db.session.commit()
