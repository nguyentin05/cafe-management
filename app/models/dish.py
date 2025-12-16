from enum import Enum as Enums
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class DishUnit(Enums):
    PIECE = "Cái"
    CUP = "Ly"

class CategoryGroup(BaseModel):
    name = Column(String(50), unique=True, nullable=False)
    categories = relationship('DishCategory', backref='categoryGroup', lazy=True)

    def __str__(self):
        return self.name

class DishCategory(BaseModel):
    name = Column(String(50), unique=True, nullable=False)
    dishes = relationship('Dish', backref='dishCategory', lazy=True)
    categoryGroup_id = Column(Integer, ForeignKey('category_group.id'), nullable=False)

    def __str__(self):
        return self.name

class Dish(BaseModel):
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    image = Column(String(200)) #nho cap nhat anh mac dinh sau khi up cloudinary
    unit = Column(Enum(DishUnit), nullable=False)
    dishCategory_id = Column(Integer, ForeignKey('dish_category.id'), nullable=False)
    details = relationship('OrderDetails', backref='dish', lazy=True)

    def __str__(self):
        return self.name