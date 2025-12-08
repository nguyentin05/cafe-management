from enum import Enum as Enums

from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum, DateTime, Text
from app.extensions import db
from sqlalchemy.orm import relationship
from datetime import datetime

class PaymentMethod(Enums):
    CASH = "CASH"
    CARD = "CARD"
    MOBILE_BANKING = "MOBILE_BANKING"

class PaymentStatus(Enums):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

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
    cash_tendered = Column(Float, nullable=True)
    change_returned = Column(Float, nullable=True)

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
        'polymorphic_identity': PaymentMethod.MOBILE_BANKING
    }


class Recipe(BaseModel):
    instruction = Column(String(500), nullable=False)
    details = relationship('RecipeDetail', backref='recipe', lazy=True)
    dish_id = Column(Integer, ForeignKey('dish.id'), nullable=False, unique=True)
    dish = relationship('Dish', back_populates='recipe')

class RecipeDetail(BaseModel):
    quantity = Column(Float, nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipe.id'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), nullable=False)
