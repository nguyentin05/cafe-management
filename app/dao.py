from app import app
from models import DishCategory, Dish

def load_dish_categories():
    return DishCategory.query.all()
