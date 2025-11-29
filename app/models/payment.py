from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.extensions import db
from sqlalchemy.orm import relationship

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class Payment(BaseModel):
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    amount = Column(Float, nullable=False)
    # method = Column('PaymentStrategy', nullable=False)

class Recipe(BaseModel):
    instruction = Column(String(500), nullable=False)
    details = relationship('RecipeDetail', backref='recipe', lazy=True)
    dish_id = Column(Integer, ForeignKey('dish.id'), nullable=False, unique=True)
    dish = relationship('Dish', back_populates='recipe')

class RecipeDetail(BaseModel):
    quantity = Column(Float, nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipe.id'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), nullable=False)
