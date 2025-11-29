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
