import cloudinary.uploader
from flask import request
from flask_admin.form import FileUploadField
from wtforms import TextAreaField
from wtforms.widgets import TextArea

class CKTextAreaWidget(TextArea):
    def __call__(self, field, *args, **kwargs):
        kwargs['class'] = (kwargs.get('class', '') + ' ckeditor5').strip()
        kwargs.setdefault('id', f'ck5_{field.id}')
        return super().__call__(field, *args, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class MyImage(FileUploadField):
    def populate_obj(self, obj, name):
        r = cloudinary.uploader.upload(request.files['image'])
        setattr(obj, name, r['secure_url'])

def get_total_session(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }

import hashlib

def hash_password(raw_password: str) -> str:
    return hashlib.md5(raw_password.strip().encode('utf-8')).hexdigest()
