from enum import Enum as Enums
from sqlalchemy import Column, Integer, DateTime, String, Float, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extensions import db


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class OrderType(Enums):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"

class OrderStatus(Enums):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    PREPARING = 'PREPARING'
    DELIVERING = 'DELIVERING'
    READY_TO_PAY = 'READY_TO_PAY'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

ORDER_STATUS_MAP = {
    OrderType.OFFLINE: [OrderStatus.CONFIRMED,
                OrderStatus.PREPARING,
                OrderStatus.READY_TO_PAY,
                OrderStatus.COMPLETED,
                OrderStatus.CANCELED],
    OrderType.ONLINE: [OrderStatus.PENDING,
                OrderStatus.CONFIRMED,
                OrderStatus.PREPARING,
                OrderStatus.DELIVERING,
                OrderStatus.COMPLETED,
                OrderStatus.CANCELED],
}

class Order(BaseModel):
    created_date = Column(DateTime, default=datetime.now)
    status = Column(Enum(OrderStatus), nullable=False)
    note = Column(Text, nullable=True)
    details = relationship('OrderDetails', backref='order', lazy=True)
    waiter_id = Column(Integer, ForeignKey('waiter.id'), nullable=True)
    # discount = Column(String(50), nullable=True, unique=True)
    payments = relationship('Payment', backref='order', lazy=True)
    order_type = Column(Enum(OrderType), nullable=False)
    __mapper_args__ = {
        'polymorphic_on': order_type,
        'polymorphic_identity': 'order'
    }

class OnlineOrder(Order):
    id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    customer_address = Column(String(255), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': OrderType.ONLINE,
    }

class OfflineOrder(Order):
    id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    table_number = Column(Integer, nullable=False)
    cashier_id = Column(Integer, ForeignKey('cashier.id'), nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': OrderType.OFFLINE,
    }

class OrderDetails(BaseModel):
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0.0)
    dish_id = Column(Integer, ForeignKey('dish.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)