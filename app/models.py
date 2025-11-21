from sqlalchemy import Column, Integer, DateTime, String, Float, Boolean, ForeignKey, Enum, Date, Text
from app import db,app
from datetime import datetime, date
from sqlalchemy.orm import relationship
from enum import Enum as Enums
from flask_login import UserMixin

class DishUnit(Enums):
    PIECE = "PIECE"
    CUP = "CUP"

class IngredientUnit(Enums):
    KG = "KG"
    L = "L"

class OrderStatus(Enums):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PREPARING = 'preparing'
    DELIVERING = 'delivering'
    READY_TO_PAY = 'ready_to_pay'
    COMPLETE = 'completed'
    CANCELED = 'cancelled'

class UserRole(Enums):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"
    EMPLOYEE = "EMPLOYEE"

class EmployeeRole(Enums):
    MANAGER = "MANAGER"
    CASHIER = "CASHIER"
    WAITER = "WAITER"

class NoteType(Enums):
    GOODS_RECEIPT = "GRN"
    GOODS_ISSUE = "GIN"
    STOCK_TRANSFER = "STN"

class OrderType(Enums):
    ONLINE = "online"
    OFFLINE = "offline"

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

class User(BaseModel, UserMixin):
    fullname = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(100),nullable=True, unique=True)
    avatar = Column(String(200))
    image = Column(String(100))# cap nhat hinh nen mac dinh
    active = Column(Boolean, default=True)
    joined_date = Column(Date, default=date.today())
    user_role = Column(Enum(UserRole), nullable=False)

    __mapper_args__ = {
        'polymorphic_on': user_role,
        'polymorphic_identity': 'user'
    }

class Employee(User):
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    employee_role = Column(Enum(EmployeeRole), nullable=False)

    @property
    def employee_code(self):
        return f"{self.role.value[0]}{self.id:04d}"

    __mapper_args__ = {
        'polymorphic_on': employee_role,
        'polymorphic_identity': UserRole.EMPLOYEE
    }

class Admin(User):
    id = Column(Integer, ForeignKey(User.id), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': UserRole.ADMIN
    }

class Customer(User):
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    online_orders = relationship('OnlineOrder', backref='customer', lazy=True)

    @property
    def customer_code(self):
        return f"{"KH"}{self.id:04d}"

    __mapper_args__ = {
        'polymorphic_identity': UserRole.CUSTOMER
    }

class Cashier(Employee):
    id = Column(Integer, ForeignKey(Employee.id), primary_key=True)
    offline_orders = relationship('OfflineOrder', backref='cashier', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': EmployeeRole.CASHIER
    }

class Manager(Employee):
    id = Column(Integer, ForeignKey(Employee.id), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': EmployeeRole.MANAGER
    }

class Waiter(Employee):
    id = Column(Integer, ForeignKey(Employee.id), primary_key=True)
    orders = relationship('Order', backref='waiter', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': EmployeeRole.WAITER
    }

class CategoryGroup(BaseModel):
    name = Column(String(50), unique=True, nullable=False)
    categories = relationship('DishCategory', backref='categoryGroup', lazy=True)

    def __str__(self):
        return self.name

class DishCategory(BaseModel):
    name = Column(String(50), unique=True, nullable=False)
    dishes = relationship('Dish', backref='dishCategory', lazy=True)
    categoryGroup_id = Column(Integer, ForeignKey(CategoryGroup.id), nullable=False)

    def __str__(self):
        return self.name

class Dish(BaseModel):
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
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
    created_date = Column(DateTime, default=datetime.now)
    status = Column(Enum(OrderStatus), nullable=False)
    note = Column(Text, nullable=True)
    details = relationship('OrderDetails', backref='order', lazy=True)
    waiter_id = Column(Integer, ForeignKey(Waiter.id), nullable=True)
    # discount = Column(String(50), nullable=True, unique=True)
    payments = relationship('Payment', backref='order', lazy=True)
    order_type = Column(Enum(OrderType), nullable=False)
    __mapper_args__ = {
        'polymorphic_on': order_type,
        'polymorphic_identity': 'order'
    }

class OnlineOrder(Order):
    id = Column(Integer, ForeignKey(Order.id), primary_key=True)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    customer_address = Column(String(255), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': OrderType.ONLINE,
    }

class OfflineOrder(Order):
    id = Column(Integer, ForeignKey(Order.id), primary_key=True)
    table_number = Column(Integer, nullable=False)
    cashier_id = Column(Integer, ForeignKey(Cashier.id), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': OrderType.OFFLINE,
    }

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
    id = Column(Integer, ForeignKey(Note.id), primary_key=True)
    ingredient_name = Column(String(100), nullable=False)
    unit = Column(String(20), nullable=False)
    quantity = Column(Float, nullable=False)
    date_created = Column(Date, default=date.today())
    __mapper_args__ = {
        'polymorphic_identity': NoteType.GOODS_RECEIPT
    }

class GoodsIssueNote(Note):
    id = Column(Integer, ForeignKey(Note.id), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': NoteType.GOODS_ISSUE
    }

class StockTransferNote(Note):
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
        cg1 = CategoryGroup(name='Foods')
        cg2 = CategoryGroup(name='Drinks')
        dc1 = DishCategory(name='Latte', categoryGroup_id=2)
        dc2 = DishCategory(name='Hot Coffee', categoryGroup_id=2)
        dc3 = DishCategory(name='Breakfast', categoryGroup_id=1)
        dc4 = DishCategory(name='Hot Chocolate', categoryGroup_id=2)
        dc5 = DishCategory(name='Bakery', categoryGroup_id=1)
        d1 = Dish(name='Latte', price=40000,
                  image='https://res.cloudinary.com/dam6k8ezg/image/upload/v1762667757/kices3owtzqzhhxqshie.jpg',
                  unit=DishUnit.CUP, dishCategory_id=1)
        d2 = Dish(name='Americano', price=40000,
                  image='https://res.cloudinary.com/dam6k8ezg/image/upload/v1762668228/nk9biuw7piporcr5ykoa.jpg',
                  unit=DishUnit.CUP, dishCategory_id=2)
        d3 = Dish(name='Matcha Latte', price=40000,
                  image='https://res.cloudinary.com/dam6k8ezg/image/upload/v1762668374/nlai0rzggdsex7bu0mxe.jpg',
                  unit=DishUnit.CUP, dishCategory_id=1)
        d4 = Dish(name='Croissant', price=40000,
                  image='https://res.cloudinary.com/dam6k8ezg/image/upload/v1762668533/qbnmz5iknk5dvuxfb8od.jpg',
                  unit=DishUnit.PIECE, dishCategory_id=5)
        d5 = Dish(name='Bacon Gouda Egg Sandwich', price=40000,
                  image='https://res.cloudinary.com/dam6k8ezg/image/upload/v1762668577/uu2adt55oktzh93j9zlb.jpg',
                  unit=DishUnit.PIECE, dishCategory_id=3)
        d6 = Dish(name='Cappuccino', price=40000,
                  image='https://res.cloudinary.com/dam6k8ezg/image/upload/v1762668604/xvifqkcn1ukgexznfpby.jpg',
                  unit=DishUnit.CUP, dishCategory_id=2)
        d7 = Dish(name='Egg Pesto Mozzarella Sandwich', price=40000,
                  image='https://res.cloudinary.com/dam6k8ezg/image/upload/v1762668656/yxfejhpbb4g3svpgtsvq.jpg',
                  unit=DishUnit.PIECE, dishCategory_id=3)
        db.session.add_all([cg1, cg2, dc1, dc2, dc3, dc4, dc5, d1, d2, d3, d4, d5, d6, d7])
        db.session.commit()