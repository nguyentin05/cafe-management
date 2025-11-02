from abc import abstractmethod, ABC
from sqlalchemy import Column, Integer, DateTime, String, Float, Boolean, ForeignKey, Enum, Date
from app import db,app
from datetime import datetime, date
from sqlalchemy.orm import relationship
from enum import Enum as Enums

class DishUnit(Enums):
    PIECE = "PIECE"
    CUP = "CUP"

class IngredientUnit(Enums):
    KG = "KG"
    L = "L"

class OrderStatus(Enums):
    WAITING = 1
    PROCESSING = 2
    READY_FOR_CHECKOUT = 3
    COMPLETE = 4
    CANCELED = 5

class EmployeeRole(Enums):
    MANAGER = "MANAGER"
    CASHIER = "CASHIER"
    WAITER = "WAITER"

class NoteType(Enums):
    GOODS_RECEIPT = "GRN"
    GOODS_ISSUE = "GIN"
    STOCK_TRANSFER = "STN"

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

class User(BaseModel):
    __abstract__ = True

    fullname = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(100),nullable=True, unique=True)
    avatar = Column(String(200))
    image = Column(String(100))# cap nhat hinh nen mac dinh
    is_active = Column(Boolean,default=True)

class Employee(User):
    __abstract__ = True

    role = Column(Enum(EmployeeRole), nullable=False)

    @property
    def employee_code(self):
        return f"{self.role.value[0]}{self.id:04d}"

class Admin(User):
    pass

class Customer(User):
    orders = relationship('Order', backref='order', lazy=True)

    @property
    def customer_code(self):
        return f"{"KH"}{self.id:04d}"

class Cashier(Employee):
    orders = relationship('Order', backref='cashier', lazy=True)

class Manager(Employee):
    pass

class Waiter(Employee):
    orders = relationship('Order', backref='waiter', lazy=True)


class DishCategory(BaseModel):
    name = Column(String(50), unique=True, nullable=False)
    dishes = relationship('Dish', backref='dishCategory', lazy=True)

    def __str__(self):
        return self.name

class Dish(BaseModel):
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200), nullable=True)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    image = Column(String(200)) #nho cap nhat anh mac dinh sau khi up cloudinary
    unit = Column(Enum(DishUnit), nullable=False)
    dishCategory_id = Column(Integer, ForeignKey(DishCategory.id), nullable=False)
    details = relationship('OrderDetails', backref='dish', lazy=True)
    recipe = relationship('Recipe', uselist=False, back_populates='dish')


    def __str__(self):
        return self.name

class Order(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    status = Column(Enum(OrderStatus), default=OrderStatus.WAITING)
    details = relationship('OrderDetails', backref='order', lazy=True)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    waiter_id = Column(Integer, ForeignKey(Waiter.id), nullable=False)
    cashier_id = Column(Integer, ForeignKey(Cashier.id), nullable=False)
    discount = Column(String(50), nullable=True, unique=True)
    payments = relationship('Payment', backref='order', lazy=True)

class OrderDetails(BaseModel):
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0.0)
    dish_id = Column(Integer, ForeignKey(Dish.id), nullable=False)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)

class Payment(BaseModel):
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)
    amount = Column(Float, nullable=False)
    # method = Column('PaymentStrategy', nullable=False)

class IngredientCategory(BaseModel):
    name = Column(String(50), unique=True, nullable=False)
    ingredients = relationship('Ingredient', backref='ingredientCategory', lazy=True)

    def __str__(self):
        return self.name

class Ingredient(BaseModel):
    name = Column(String(50), unique=True, nullable=False)
    cost = Column(Float, nullable=False)
    description = Column(String(200), nullable=True)
    unit = Column(Enum(IngredientUnit), nullable=False)
    ingredientCategory_id = Column(Integer, ForeignKey(IngredientCategory.id), nullable=False)
    detailsRecipe = relationship('RecipeDetail', backref='ingredient', lazy=True)
    detailsStorage = relationship('StorageDetail', backref='ingredient', lazy=True)
    detailsNote = relationship('NoteDetail', backref='ingredient', lazy=True)
    detailsInventoryReport = relationship('InventoryReportDetail', backref='ingredient', lazy=True)

    def __str__(self):
        return self.name

class Recipe(BaseModel):
    instruction = Column(String(500), nullable=False)
    details = relationship('RecipeDetail', backref='recipe', lazy=True)
    dish_id = Column(Integer, ForeignKey(Dish.id), nullable=False, unique=True)
    dish = relationship('Dish', back_populates='recipe')

class RecipeDetail(BaseModel):
    quantity = Column(Float, nullable=False)
    recipe_id = Column(Integer, ForeignKey(Recipe.id), nullable=False)
    ingredient_id = Column(Integer, ForeignKey(Ingredient.id), nullable=False)

class Storage(BaseModel):
    name = Column(String(50), unique=True, nullable=False)
    address = Column(String(100), nullable=True, unique=True)
    details = relationship('StorageDetail', backref='storage', lazy=True)

class StorageDetail(BaseModel):
    quantity = Column(Float, default=0)
    ingredient_id = Column(Integer, ForeignKey(Ingredient.id), nullable=False)
    Storage = Column(Integer, ForeignKey(Storage.id), nullable=False)

class Note(BaseModel):
    type = Column(Enum(NoteType), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    details = relationship('NoteDetail', backref='note', lazy=True)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'note'
    }

class GoodsReceiptNote(Note):
    __tablename__ = 'goods_receipt_note'
    id = Column(Integer, ForeignKey(Note.id), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': NoteType.GOODS_RECEIPT
    }

class GoodsIssueNote(Note):
    __tablename__ = 'goods_issue_note'
    id = Column(Integer, ForeignKey(Note.id), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': NoteType.GOODS_ISSUE
    }

class StockTransferNote(Note):
    __tablename__ = 'stock_transfer_note'
    id = Column(Integer, ForeignKey(Note.id), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': NoteType.STOCK_TRANSFER
    }

class NoteDetail(BaseModel):
    quantity = Column(Float, default=0)
    note_id = Column(Integer, ForeignKey(Note.id), nullable=False)
    ingredient_id = Column(Integer, ForeignKey(Ingredient.id), nullable=False)

class InventoryReport(BaseModel):
    created_date = Column(Date, default=date.today())
    details = relationship('InventoryReportDetail', backref='inventoryReport', lazy=True)

class InventoryReportDetail(BaseModel):
    quantity = Column(Float, default=0)
    inventoryReport_id = Column(Integer, ForeignKey(InventoryReport.id), nullable=False)
    ingredient_id = Column(Integer, ForeignKey(Ingredient.id), nullable=False)

# class PaymentStrategy(db.Model, ABC):
#     __abstract__ = True
#
#     @abstractmethod
#     def pay(self, amount):
#         pass

# class CashPayment(PaymentStrategy):
#     def pay(self, amount):
#         pass
#
# class CreditCardPayment(PaymentStrategy):
#     def pay(self, amount):
#         pass
#
# class MobileBankingPayment(PaymentStrategy):
#     def pay(self, amount):
#         pass


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()