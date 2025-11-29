from app.models.user import User, Customer
from app.extensions import db
from app.utils import hash_password

def add_customer(fullname, username, password, **kwargs):
    password = hash_password(password)
    customer = Customer(fullname = fullname.strip(),
                username = username.strip(),
                password = password,
                phone = kwargs.get('phone'))

    db.session.add(customer)
    db.session.commit()

def auth_user(username, password, role=None):
    password = hash_password(password)

    u = User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password))

    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()

def get_user_by_id(id):
    return User.query.get(id)

def get_customer_by_id(id):
    return Customer.query.get(id)

def update_customer_info(customer_id, **kwargs):
    customer = get_customer_by_id(customer_id)

    if not customer:
        raise Exception('Customer not found.')


    customer.fullname = kwargs.get('fullname')
    customer.phone = kwargs.get('phone')
    customer.address = kwargs.get('address')
    customer.email = kwargs.get('email')
    customer.dob = kwargs.get('dob')
    customer.gender = kwargs.get('gender')

    try:
        db.session.commit()
        return customer
    except Exception as ex:
        db.session.rollback()
        raise ex