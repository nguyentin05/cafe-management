import cloudinary.uploader
from flask import request
from flask_admin.form import FileUploadField
from wtforms import TextAreaField
from wtforms.widgets import TextArea

class CKTextAreaWidget(TextArea):
    def __call__(self, field, *args, **kwargs):
        # if kwargs.get('class'):
        #     kwargs['class'] += ' ckeditor'
        # else:
        #     kwargs.setdefault('class', 'ckeditor')
        #
        # return super().__call__(field=field, **kwargs)

        # CKEditor 5 sẽ tìm theo class này
        kwargs['class'] = (kwargs.get('class', '') + ' ckeditor5').strip()
        # nên đặt id để init nhiều editor
        kwargs.setdefault('id', f'ck5_{field.id}')
        return super().__call__(field, *args, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class MyImage(FileUploadField):
    def populate_obj(self, obj, name):
        r = cloudinary.uploader.upload(request.files['image'])
        setattr(obj, name, r['secure_url'])