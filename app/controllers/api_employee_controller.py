from flask import Blueprint,jsonify,request
from flask_login import login_required
from app.daos.order_dao import add_offline_order
from app.decorators import waiter_required

api_employee = Blueprint('api_employee', __name__)

@api_employee.route('/complete', methods=['post'])
@login_required
@waiter_required
def complete():
    data = request.json
    table = data.get('table')
    note = data.get('note', '')
    draft = data.get('draft')

    try:
        if not draft:
            return jsonify({'code': 400, 'message': 'Gio hang rong'})

        add_offline_order(draft, note=note, table=table)
    except Exception as ex:
        print(str(ex))
        return jsonify({'code': 400})

    return jsonify({'code': 200})