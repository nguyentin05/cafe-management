from flask_admin.contrib.sqla import ModelView
from app import db, admin
from utils import CKTextAreaField, MyImage
from models import Dish, DishCategory

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

admin.add_view(DishView(Dish, db.session))
admin.add_view(ModelView(DishCategory, db.session))
