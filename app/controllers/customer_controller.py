from flask import render_template, Blueprint, flash, redirect, url_for, request, session, jsonify
from flask_login import login_required, current_user

from app import db, get_total_session, get_value
from app.daos.order_dao import update_online_order, get_online_order_by_status, get_online_order_by_id, \
    get_offline_order_by_id
from app.daos.payment_dao import get_payment_by_id_and_method_and_status
from app.daos.user_dao import update_customer_info
from app.decorators import customer_required
from app.forms import CustomerEditForm, OrderForm
from app.models import OnlineOrder, OrderStatus, PaymentMethod, PaymentStatus, MomoPayment, OrderType

customer = Blueprint('customer', __name__)

@customer.route('/info')
@login_required
@customer_required
def info():
    return render_template('customer/info.html')

@customer.route('/checkout/<order_id>', methods=['get'])
@login_required
@customer_required
def checkout(order_id):
    order = get_online_order_by_id(id=order_id, customer_id=current_user.id)

    if not order or order.status != OrderStatus.UNPAID:
        flash('Đơn hàng không hợp lệ.', 'warning')
        return redirect(url_for('customer.cart'))

    return render_template('customer/checkout.html', order=order)

@customer.route('/cart', methods=['get', 'post'])
@login_required
@customer_required
def cart():
    form = OrderForm()

    cart = session.get('cart')

    if not cart:
        cart = {}

    if form.validate_on_submit():
        total_stats = get_total_session(cart=cart)
        total_quantity = total_stats['total_quantity']

        MAX_QUANTITY = int(get_value('MAX_QUANTITY'))

        if total_quantity > MAX_QUANTITY:
            flash(f'Giỏ hàng vượt quá {MAX_QUANTITY} món!', 'danger')
            return render_template('customer/cart.html', form=form)

        try:
            id = update_online_order(
                cart=cart,
                customer_id=current_user.id,
                address=form.address.data,
                note=form.note.data
            )
            return redirect(url_for('customer.checkout', order_id=id))
        except Exception as e:
            flash('Lỗi hệ thống, vui lòng thử lại.', 'danger')

    if request.method.__eq__('GET'):
        order = get_online_order_by_status(status=OrderStatus.UNPAID, customer_id=current_user.id)

        if order:
            if not form.address.data:
                form.address.data = order.customer_address
            if not form.note.data:
                form.note.data = order.note

    return render_template('customer/cart.html', form=form)

@customer.route("/orders/<int:id>")
@login_required
@customer_required
def order_detail(id):
    return render_template("customer/order_detail.html")

@customer.route('/info/edit', methods=['get', 'post'])
@login_required
@customer_required
def edit_info():
    form = CustomerEditForm(obj=current_user)
    form.user_id.data = current_user.id
    err_msg = ''
    if form.validate_on_submit():
        try:
            update_customer_info(
                customer_id = current_user.id,
                fullname = form.fullname.data,
                phone = form.phone.data,
                address = form.address.data,
                email = form.email.data,
                dob = form.dob.data,
                gender = form.gender.data or None,
            )
            flash('Cập nhật thông tin thành công!', 'success')
            return redirect(url_for('auth.info'))
        except Exception as ex:
            err_msg = 'he thong loi' + str(ex)
            flash(err_msg, 'danger')

    return render_template("customer/edit-info.html", form=form, err_msg=err_msg)


@customer.route('/payment/momo-return', methods=['get'])
def momo_return():
    result_code = request.args.get('resultCode')
    momo_order_id = request.args.get('orderId')
    message = request.args.get('message')

    order_id = momo_order_id.split('_')[0]

    order = get_online_order_by_id(id=order_id, customer_id=current_user.id)

    if not order:
        order = get_offline_order_by_id(id=order_id)

    if not order:
        return "Order not found", 404

    current_payment = get_payment_by_id_and_method_and_status(order_id, PaymentMethod.MOBILE_BANKING, PaymentStatus.PENDING)

    if result_code == '0':
        if current_payment:
            current_payment.status = PaymentStatus.SUCCESS

        if order.order_type == OrderType.ONLINE:
            order.status = OrderStatus.PENDING

            db.session.commit()
            session.pop('cart', None)
            return render_template('customer/payment-success.html', order=order)

        elif order.order_type == OrderType.OFFLINE:
            order.status = OrderStatus.COMPLETED

            db.session.commit()
            flash("Thanh toán thành công! Đơn hàng đã hoàn tất.", "success")
            return render_template('customer/payment-success.html', order=order)

    else:
        if current_payment:
            current_payment.status = PaymentStatus.FAILED

        db.session.commit()

        flash(f'Giao dịch thất bại: {message}', 'danger')

        if order.order_type == OrderType.ONLINE:
            return redirect(url_for('customer.checkout', order_id=order_id))
        else:
            return redirect(url_for('employee_web.order_detail', id=order_id))