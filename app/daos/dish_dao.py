from sqlalchemy import func, extract, cast, Date

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

def dish_stat_by_day(from_date=None, to_date=None):
    query = db.session.query(Dish.name, func.sum(OrderDetails.quantity * OrderDetails.unit_price), func.sum(OrderDetails.quantity))\
                      .join(OrderDetails, OrderDetails.dish_id.__eq__(Dish.id), isouter=True)\
                      .join(Order, Order.id.__eq__(OrderDetails.order_id))\
                      .group_by(Dish.name)

    if from_date:
        query = query.filter(Order.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(cast(Order.created_date, Date).__le__(to_date))

    return query.all()

def dish_stats_by_month(month, year):
    return db.session.query(Dish.name, func.sum(OrderDetails.quantity))\
                      .join(OrderDetails, OrderDetails.dish_id.__eq__(Dish.id), isouter=True)\
                      .join(Order, Order.id.__eq__(OrderDetails.order_id))\
                      .filter(extract('month', Order.created_date) == month,
                              extract('year', Order.created_date) == year)\
                      .group_by(Dish.name).all()

def dish_count_by_month(month, year):
    return db.session.query(func.sum(OrderDetails.quantity))\
                     .join(Order, OrderDetails.order_id.__eq__(Order.id))\
                     .filter(extract('month', Order.created_date) == month,
                             extract('year', Order.created_date) == year)\
                     .scalar() or 0