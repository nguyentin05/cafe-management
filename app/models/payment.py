from enum import Enum as Enums

from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum, DateTime, Text
from app.extensions import db
from sqlalchemy.orm import relationship
from datetime import datetime

class PaymentMethod(Enums):
    CASH = "Tiền mặt"
    CARD = "Thẻ tín dụng"
    MOMO = "Momo"

class PaymentStatus(Enums):
    PENDING = "Đang chờ"
    SUCCESS = "Thành công"
    FAILED = "Thất bại"

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class Payment(BaseModel):
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    amount = Column(Integer, nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False)
    method = Column(Enum(PaymentMethod), nullable=False)

    __mapper_args__ = {
        'polymorphic_on': method,
        'polymorphic_identity': 'payment'
    }

class CashPayment(Payment):
    id = Column(Integer, ForeignKey('payment.id'), primary_key=True)
    cash_tendered = Column(Integer, nullable=True)
    change_returned = Column(Integer, nullable=True)
    # cashier_id = Column(Integer, ForeignKey('cashier.id'), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': PaymentMethod.CASH
    }

class CardPayment(Payment):
    id = Column(Integer, ForeignKey('payment.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': PaymentMethod.CARD
    }

class MomoPayment(Payment):
    id = Column(Integer, ForeignKey('payment.id'), primary_key=True)
    request_id = Column(String(100), unique=True, nullable=False)
    pay_url = Column(Text, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': PaymentMethod.MOMO
    }