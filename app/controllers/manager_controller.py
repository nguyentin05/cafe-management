from datetime import date, datetime, timedelta

from flask import Blueprint, render_template, request
from flask_login import login_required
from app.daos.dish_dao import dish_stat_by_day, dish_stats_by_month, dish_count_by_month
from app.daos.inventory_dao import get_report_by_day, get_grn_by_day, get_ingredient_by_id
from app.daos.order_dao import count_order_by_time, revenue_month_stats, revenue_by_day
from app.decorators import manager_required

manager = Blueprint('manager', __name__)


@manager.route('/stats_revenue')
@login_required
@manager_required
def stats_revenue():
    option = request.args.get('option', 'custom')
    from_date = request.args.get('from_date', date.today())
    to_date = request.args.get('to_date', date.today())
    year = request.args.get('year', datetime.now().year)

    if option == 'year':
        stats = revenue_month_stats(year=year)
        from_date = f"{year}-01-01"
        to_date = f"{year}-12-31"

    elif option == 'custom':
        stats = dish_stat_by_day(from_date=from_date, to_date=to_date)

    order_count = count_order_by_time(from_date=from_date, to_date=to_date)
    revenue = revenue_by_day(from_date=from_date, to_date=to_date)

    return render_template('manager/stats-revenue.html',
                           stats=stats, order_count=order_count, revenue=revenue, from_date=from_date, to_date=to_date,
                           option=option,
                           year=year)


@manager.route('/stats-dish')
@login_required
@manager_required
def stats_dish():
    month = request.args.get('month', datetime.now().month)
    year = request.args.get('year', datetime.now().year)

    stats = dish_stats_by_month(month, year)
    dish_count = dish_count_by_month(month, year)

    return render_template('manager/stats-dish.html', stats=stats, dish_count=dish_count, month=month, year=year)


@manager.route('/stats_report')
@login_required
@manager_required
def stats_report():
    day = request.args.get('date')

    if day:
        try:
            day = datetime.strptime(day, '%Y-%m-%d').date()
        except ValueError:
            day = date.today() - timedelta(days=1)
    else:
        day = date.today() - timedelta(days=1)

    prev_day = day - timedelta(days=1)

    tonDau = get_report_by_day(prev_day)

    tonCuoi = get_report_by_day(day)

    tonNhap = get_grn_by_day(day)

    ids = set(tonCuoi.keys()) | set(tonDau.keys()) | set(tonNhap.keys())

    rows = []
    index = 1

    for id in ids:
        ing = get_ingredient_by_id(id)

        slTonDau = tonDau.get(id, 0.0)
        slTonNhap = tonNhap.get(id, 0.0)
        slTonCuoi = tonCuoi.get(id, 0.0)

        slTonXuat = slTonDau + slTonNhap - slTonCuoi

        rows.append({
            'index': index,
            'id': id,
            'name': ing.name,
            'unit': ing.unit.value,
            'cost': ing.cost,
            'tonDau': slTonDau,
            'tonNhap': slTonNhap,
            'tonXuat': slTonXuat,
            'tonCuoi': slTonCuoi
        })
        index += 1

    return render_template('manager/stats-report.html', rows=rows, date=day)
