from app import app
from models import Category, Dish

def load_categories():
    return Category.query.all()
