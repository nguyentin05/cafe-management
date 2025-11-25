from app.models.user import User, Customer
from app.extensions import db
from app.utils import hash_password

def add_customer(fullname, username, password, **kwargs):
    password = hash_password(password)
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