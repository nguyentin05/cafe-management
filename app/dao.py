from app import app, db
from models import DishCategory, Dish, User, UserRole
import hashlib

def load_dish_categories():
    return DishCategory.query.all()

def get_dish_by_id(id):
    return Dish.query.get(id)

def add_customer(fullname, username, password, **kwargs):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    user = User(fullname = fullname.strip(),
                username = username.strip(),
                password = password,
                user_role = UserRole.CUSTOMER,
                email = kwargs.get('email'))

    db.session.add(user)
    db.session.commit()

def check_login(username, password):
    if username and password:
        password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

def get_user_by_id(id):
    return User.query.get(id)