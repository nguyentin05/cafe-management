from flask import redirect
from flask_admin import BaseView, expose, AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user
from wtforms import PasswordField

from .extensions import db
from .models import UserRole, Ingredient
from .models.order import Regulation
from .utils import MyImage, hash_password, CKTextAreaField
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

class IngredientView(AuthenticatedView):
    column_list = ["name", "cost", 'is_active']
    can_view_details = True
    form_columns = (
        'name', 'description', 'cost', 'is_active', 'unit'
    )
    extra_js = ['//cdn.ckeditor.com/ckeditor5/41.0.0/classic/ckeditor.js',
                '/static/js/admin_ckeditor5_init.js',]
    form_overrides = {
        'description': CKTextAreaField
    }

class DishCategoryView(AuthenticatedView):
    column_list = ["name", "dishes"]
    column_searchable_list = ['name']
    column_filters = ['name']
    column_labels = {
        "name": "Tên loại",
        "dishes": "Danh sách món ăn"
    }

class RegulationView(AuthenticatedView):
    can_view_details = True

class UserView(AuthenticatedView):
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = hash_password(form.password.data)

class EmployeeView(AuthenticatedView):
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    form_overrides = {
        'avatar': MyImage
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = hash_password(form.password.data)

class MyLogoutView(BaseView):
    @expose('/')
    def index(self) -> str:
        logout_user()
        return redirect("/admin")

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self) -> str:
        return self.render('admin/index.html')

admin = Admin(name='Cafe Administration', theme=Bootstrap4Theme(), index_view=MyAdminIndexView())

def init_admin(app):
    admin.add_view(DishView(Dish, db.session))
    admin.add_view(UserView(User, db.session))
    admin.add_view(EmployeeView(Employee, db.session))
    admin.add_view(DishCategoryView(DishCategory, db.session))
    admin.add_view(IngredientView(Ingredient, db.session))
    admin.add_view(RegulationView(Regulation, db.session))
    admin.add_view(MyLogoutView('Đăng xuất'))
    admin.init_app(app)
