from functools import wraps
from flask import request, url_for, redirect, abort
from flask_login import current_user
from app.models.user import UserRole, EmployeeRole

def user_role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.signin'))

            if current_user.user_role not in roles:
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return user_role_required(UserRole.ADMIN)(f)

def customer_required(f):
    return user_role_required(UserRole.CUSTOMER)(f)

def employee_required(f):
    return user_role_required(UserRole.EMPLOYEE)(f)

def employee_role_required(*emplyee_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.signin'))

            if current_user.user_role != UserRole.EMPLOYEE:
                abort(403)

            role = getattr(current_user, 'employee_role', None)
            if role not in emplyee_roles:
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def cashier_required(f):
    return employee_role_required(EmployeeRole.CASHIER)(f)

def manager_required(f):
    return employee_role_required(EmployeeRole.MANAGER)(f)

def waiter_required(f):
    return employee_role_required(EmployeeRole.WAITER)(f)