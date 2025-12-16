from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import PasswordField

from .extensions import db
from .models import UserRole
from .models.order import Regulation
from .utils import MyImage, hash_password, CKTextAreaField, CKTextAreaWidget
from .models.dish import Dish, DishCategory
from .models.user import User, Employee

class AuthenticatedView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class DishView(AuthenticatedView):
    column_list = ["name", "price", 'is_active']
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

class MyCategoryView(AuthenticatedView):
    column_list = ["name", "dishes"]
    column_searchable_list = ['name']
    column_filters = ['name']
    column_labels = {
        "name": "Tên loại",
        "dishes": "Danh sách món ăn"
    }

class RegulationView(ModelView):
    can_view_details = True

class UserView(ModelView):
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = hash_password(form.password.data)

class EmployeeView(ModelView):
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = hash_password(form.password.data)

def init_admin(admin_instance):
    admin_instance.add_view(DishView(Dish, db.session))
    admin_instance.add_view(UserView(User, db.session))
    admin_instance.add_view(EmployeeView(Employee, db.session))
    admin_instance.add_view(MyCategoryView(DishCategory, db.session))
    admin_instance.add_view(RegulationView(Regulation, db.session))
