from datetime import date, datetime

from flask import Blueprint, render_template, request

from app.daos.dish_dao import dish_stats
from app.daos.order_dao import count_order_by_time, revenue_month_stats, revenue_by_day

manager = Blueprint('manager', __name__)


@manager.route('/revenue')
def revenue_stats():
    option = request.args.get('option', 'custom')
    from_date = request.args.get('from_date', datetime.now().day)
    to_date = request.args.get('to_date', datetime.now().day)
    year = request.args.get('year', datetime.now().year)

    if option == 'year':
        stats = revenue_month_stats(year=year)
        from_date=f"{year}-01-01"
        to_date = f"{year}-12-31"

    elif option == 'custom':
        stats = dish_stats(from_date=from_date, to_date=to_date)

    order_count = count_order_by_time(from_date=from_date, to_date=to_date)
    revenue = revenue_by_day(from_date=from_date, to_date=to_date)

    return render_template('manager/stats-revenue.html',
                           stats=stats, order_count=order_count, revenue=revenue, from_date=from_date, to_date=to_date, option=option,
                           year=year)