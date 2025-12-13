from sqlalchemy import func, extract

from app import db
from app.models.order import OrderDetails, Order
from app.models.dish import Dish, DishCategory, CategoryGroup

def load_dish_categories():
    return DishCategory.query.all()

def load_dishes(dish_cate=None):
    query = Dish.query

    if dish_cate:
        query = query.filter(Dish.dishCategory_id.__eq__(dish_cate))

    return query.all()

def get_dish_by_id(id):
    return Dish.query.get(id)

def get_dish_category_by_id(id):
    return DishCategory.query.get(id)

def load_category_groups():
    return CategoryGroup.query.all()

def count_dishes(dishes):
    total = 0
    for d in dishes:
        total += int(d.get('quantity'))

    return total

def dish_stats(from_date=None, to_date=None):
    query = db.session.query(Dish.name, func.sum(OrderDetails.quantity), func.sum(OrderDetails.quantity * OrderDetails.unit_price), func.count(Order.id))\
                      .join(OrderDetails, OrderDetails.dish_id.__eq__(Dish.id), isouter=True)\
                      .join(Order, Order.id.__eq__(OrderDetails.order_id))\
                      .group_by(Dish.name)

    if from_date:
        query = query.filter(extract('day', Order.created_date).__ge__(from_date))

    if to_date:
        query = query.filter(extract('day', Order.created_date).__le__(to_date))

    return query.all()

