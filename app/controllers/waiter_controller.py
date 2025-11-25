from flask import render_template, Blueprint
from app.daos.dish_dao import load_dishes

waiter = Blueprint('waiter_web', __name__)

@waiter.route('/goods-receipt-note')
def goods_receipt_note():
    return render_template('waiter/goods-receipt-note.html')

@waiter.route('/offline-order')
def offline_order():
    dishes = load_dishes()
    return render_template('waiter/offline-order.html', dishes=dishes)