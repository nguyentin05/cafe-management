from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user

from app.daos.user_dao import update_customer_info
from app.decorators import customer_required
from app.forms import CustomerEditForm

customer = Blueprint('customer', __name__)

@customer.route('/info')
@login_required
@customer_required
def info():
    return render_template('customer/info.html')

@customer.route('/cart', methods=['get', 'post'])
@login_required
@customer_required
def cart():
    return render_template('customer/cart.html')

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