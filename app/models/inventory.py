from enum import Enum as Enums
from sqlalchemy import Column, Integer, DateTime, String, Float, ForeignKey, Enum, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class IngredientUnit(Enums):
    KG = "KG"
    L = "L"

class NoteType(Enums):
    GOODS_RECEIPT = "GRN"
    GOODS_ISSUE = "GIN"
    STOCK_TRANSFER = "STN"

class Ingredient(BaseModel):
    name = Column(String(50), unique=True, nullable=False)
    cost = Column(Float, nullable=False)
    description = Column(String(200), nullable=True)
    created_date = Column(DateTime, default=datetime.now())
    unit = Column(Enum(IngredientUnit), nullable=False)
    detailsNote = relationship('NoteDetail', backref='ingredient', lazy=True)
    detailsInventoryReport = relationship('InventoryReportDetail', backref='ingredient', lazy=True)

    def __str__(self):
        return self.name

class Note(BaseModel):
    note_type = Column(Enum(NoteType), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    details = relationship('NoteDetail', backref='note', lazy=True)

    __mapper_args__ = {
        'polymorphic_on': note_type,
        'polymorphic_identity': 'note'
    }

class GoodsReceiptNote(Note):
    id = Column(Integer, ForeignKey('note.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': NoteType.GOODS_RECEIPT
    }

class GoodsIssueNote(Note):
    id = Column(Integer, ForeignKey('note.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': NoteType.GOODS_ISSUE
    }

class StockTransferNote(Note):
    id = Column(Integer, ForeignKey('note.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': NoteType.STOCK_TRANSFER
    }

class NoteDetail(BaseModel):
    quantity = Column(Float, default=0.0)
    unit_cost = Column(Float, default=0.0)
    note_id = Column(Integer, ForeignKey('note.id'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), nullable=False)

class InventoryReport(BaseModel):
    created_date = Column(Date, default=date.today())
    details = relationship('InventoryReportDetail', backref='inventoryReport', lazy=True)

class InventoryReportDetail(BaseModel):
    quantity = Column(Float, default=0.0)
    unit_cost = Column(Float, default=0.0)
    inventoryReport_id = Column(Integer, ForeignKey('inventory_report.id'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), nullable=False)