from datetime import date

from flask import render_template, Blueprint
from flask_login import login_required, current_user

from app import redis_client
from app.daos.dish_dao import load_dishes
from app.daos.inventory_dao import load_ingredients, get_grn_by_ingredient_id
from app.decorators import waiter_required
import json

waiter = Blueprint('waiter_web', __name__)


@waiter.route('/goods-receipt')
@login_required
@waiter_required
def goods_receipt():
    ingredients = load_ingredients()
    return render_template('waiter/goods-receipt.html', ingredients=ingredients)


@waiter.route('/offline-order')
@login_required
@waiter_required
def offline_order():
    dishes = load_dishes()
    return render_template('waiter/offline-order.html', dishes=dishes)


@waiter.route('/report-inventory')
@login_required
@waiter_required
def report_inventory():
    today = date.today().isoformat()
    key = f'inventory_report:{today}:{current_user.id}'

    redis_data = redis_client.hgetall(key)

    rows = []

    index = 1

    for k, v in redis_data.items():
        obj = json.loads(v)

        ingredient_id = obj.get('id')
        grn = get_grn_by_ingredient_id(id=ingredient_id, day=today)

        obj['index'] = index

        if grn:
            obj['grn'] = grn.quantity
        else:
            obj['grn'] = 0

        rows.append(obj)
        index += 1

    ingredients = load_ingredients()

    return render_template('waiter/report-inventory.html', ingredients=ingredients, rows=rows)