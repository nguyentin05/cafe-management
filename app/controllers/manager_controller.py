from datetime import datetime

from flask import Blueprint, render_template, request

from app.daos.dish_dao import dish_stats
from app.daos.order_dao import count_order_by_time, stats_revenue_by_hour, revenue_by_time

manager = Blueprint('manager', __name__)


@manager.route('/revenue')
def revenue_stats():
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    stats = dish_stats(from_date=from_date, to_date=to_date)
    order_count = count_order_by_time(from_date=from_date, to_date=to_date)
    revenue = revenue_by_time(from_date=from_date, to_date=to_date)
    another = stats_revenue_by_hour(datetime.now().day)

    return render_template('manager/stats-revenue.html',
                           stats=stats, order_count=order_count, revenue=revenue, another=another)
