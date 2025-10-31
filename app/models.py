from sqlalchemy import Column, Integer, DateTime, String, Float, Boolean, ForeignKey
from app import db
from datetime import datetime
from sqlalchemy.orm import relationship

class BaseModel(db.Model):

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    name = Column(String(50), unique=True, nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200), nullable=True)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    image = Column(String(200), nullable=False) #nho cap nhat anh mac dinh sau khi up cloudinary
    category_id = Column(Integer, ForeignKey(Category.id),nullable=False)
    details = relationship('ReceiptDetails', backref='product', lazy=True)

    def __str__(self):
        return self.name

class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)

class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0.0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
