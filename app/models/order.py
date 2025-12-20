from enum import Enum as Enums
from sqlalchemy import Column, Integer, DateTime, String, Float, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extensions import db


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class RegulationKey(Enums):
    MAX_QUANTITY = "MAX_QUANTITY"
    SERVICE_FEE_PERCENT = "SERVICE_FEE_PERCENT"
    MIN_INGREDIENT = 'MIN_INGREDIENT'

class OrderType(Enums):
    ONLINE = "Trực tuyến"
    OFFLINE = "Trực tiếp"

class LogType(Enums):
    CREATED = "Đã tạo"
    CHANGED_STATUS = "Đã đổi trạng thái"
    EDITED = "Đã sửa"
    CANCELED = "Đã hủy"

class OrderStatus(Enums):
    UNPAID = 'Chưa thanh toán'
    PENDING = 'Đang chờ'
    CONFIRMED = 'Đã xác nhận'
    PREPARING = 'Đang chuẩn bị'
    DELIVERING = 'Đang giao'
    READY_TO_PAY = 'Sẵn sàng thanh toán'
    COMPLETED = 'Hoàn thành'
    CANCELED = 'Đã hủy'

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
    # discount = Column(String(50), nullable=True, unique=True)
    payments = relationship('Payment', backref='order', lazy=True)
    order_type = Column(Enum(OrderType), nullable=False)
    order_logs = relationship('OrderLog', backref='order', lazy=True)

    @property
    def is_editable(self):
        return self.status in [
            OrderStatus.PENDING,
            OrderStatus.CONFIRMED,
            OrderStatus.PREPARING
        ]

    @property
    def total_amount(self):
        total = 0

        for d in self.details:
            total += d.unit_price * d.quantity

        return total

    @property
    def total_quantity(self):
        total = 0
        for d in self.details:
            total += d.quantity
        return total


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

    __mapper_args__ = {
        'polymorphic_identity': OrderType.OFFLINE,
    }

class OrderDetails(BaseModel):
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0.0)
    dish_id = Column(Integer, ForeignKey('dish.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)

class OrderLog(BaseModel):
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    action_type = Column(Enum(LogType), nullable=False)
    from_status = Column(Enum(OrderStatus), nullable=True)
    to_status = Column(Enum(OrderStatus), nullable=True)
    description = Column(Text, nullable=True)

class Regulation(BaseModel):
    key = Column(Enum(RegulationKey), nullable=False)
    value = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)