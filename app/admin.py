from flask_admin.theme import Bootstrap4Theme
from flask_admin.contrib.sqla import ModelView
from app import app, db, admin
from flask_admin import Admin
from models import Dish, DishCategory


admin.add_view(ModelView(Dish, db.session))
admin.add_view(ModelView(DishCategory, db.session))
