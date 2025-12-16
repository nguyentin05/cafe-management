from datetime import date
from enum import Enum as Enums
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class Gender(Enums):
    MALE = "Nam"
    FEMALE = "Nữ"

class UserRole(Enums):
    ADMIN = "Quản trị viên"
    CUSTOMER = "Khách hàng"
    EMPLOYEE = "Nhân viên"

class EmployeeRole(Enums):
    MANAGER = "Quản lý"
    CASHIER = "Thu ngân"
    WAITER = "Phục vụ"

class User(BaseModel, UserMixin):
    fullname = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(100), nullable=True, unique=True)
    avatar = Column(String(200), default='https://res.cloudinary.com/dam6k8ezg/image/upload/v1764155710/defaultAvatar_l5nyci.jpg')
    phone = Column(String(10), unique=True, nullable=False)
    active = Column(Boolean, default=True)
    joined_date = Column(Date, default=date.today())
    user_role = Column(Enum(UserRole), nullable=False)
    dob = Column(Date, nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    address = Column(String(100), nullable=True)

    @property
    def is_admin(self):
        return self.user_role == UserRole.ADMIN

    @property
    def is_employee(self):
        return self.user_role == UserRole.EMPLOYEE

    @property
    def is_customer(self):
        return self.user_role == UserRole.CUSTOMER

    __mapper_args__ = {
        'polymorphic_on': user_role,
        'polymorphic_identity': 'user'
    }

class Employee(User):
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    identity_card = Column(String(12), unique=True)
    employee_role = Column(Enum(EmployeeRole), nullable=False)
    order_logs = relationship('OrderLog', backref='employee', lazy=True)

    @property
    def employee_code(self):
        return f"{self.role.value[0]}{self.id:04d}"

    @property
    def is_manager(self):
        return self.employee_role == EmployeeRole.MANAGER

    @property
    def is_cashier(self):
        return self.employee_role == EmployeeRole.CASHIER

    @property
    def is_waiter(self):
        return self.employee_role == EmployeeRole.WAITER

    __mapper_args__ = {
        'polymorphic_on': employee_role,
        'polymorphic_identity': UserRole.EMPLOYEE
    }

class Admin(User):
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': UserRole.ADMIN
    }

class Customer(User):
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    online_orders = relationship('OnlineOrder', backref='customer', lazy=True)

    @property
    def customer_code(self):
        return f"{"KH"}{self.id:04d}"

    __mapper_args__ = {
        'polymorphic_identity': UserRole.CUSTOMER
    }

class Cashier(Employee):
    id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    offline_orders = relationship('OfflineOrder', backref='cashier', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': EmployeeRole.CASHIER
    }

class Manager(Employee):
    id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    graduation_certificate = Column(String(12), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': EmployeeRole.MANAGER
    }

class Waiter(Employee):
    id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    driver_license = Column(String(12), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': EmployeeRole.WAITER
    }