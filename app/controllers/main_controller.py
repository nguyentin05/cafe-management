from flask import Blueprint, render_template, request
from app.daos.dish_dao import load_dishes, get_dish_category_by_id

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('main/home.html')

@main.route('/menu')
def menu():
    dish_cate = request.args.get('dishCate')
    current_cate = get_dish_category_by_id(dish_cate) if dish_cate else None
    dishes = load_dishes(dish_cate)
    return render_template('main/menu.html', dishes=dishes, current_cate=current_cate)



