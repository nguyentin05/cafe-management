from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField

from .extensions import db
from .utils import CKTextAreaField, MyImage, hash_password
from .models.dish import Dish, DishCategory
from .models.user import User, Employee, Waiter

class DishView(ModelView):
    can_view_details = True
    form_columns = (
        'name', 'description', 'price', 'is_active', 'image', 'unit', 'dishCategory'
    )
    extra_js = ['//cdn.ckeditor.com/ckeditor5/41.0.0/classic/ckeditor.js',
                '/static/js/admin_ckeditor5_init.js',]
    form_overrides = {
        'description': CKTextAreaField,
        'image': MyImage
    }

class UserView(ModelView):
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    def on_model_change(self, form, model, is_created):
        # Nếu admin có nhập mật khẩu mới
        if form.password.data:
            model.password = hash_password(form.password.data)

class EmployeeView(ModelView):
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    def on_model_change(self, form, model, is_created):
        # Nếu admin có nhập mật khẩu mới
        if form.password.data:
            model.password = hash_password(form.password.data)

class WaiterView(ModelView):
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    def on_model_change(self, form, model, is_created):
        # Nếu admin có nhập mật khẩu mới
        if form.password.data:
            model.password = hash_password(form.password.data)

def init_admin(admin_instance):
    admin_instance.add_view(DishView(Dish, db.session))
    admin_instance.add_view(UserView(User, db.session))
    admin_instance.add_view(EmployeeView(Employee, db.session))
    admin_instance.add_view(WaiterView(Waiter, db.session))
    admin_instance.add_view(ModelView(DishCategory, db.session))
