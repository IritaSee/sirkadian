from config import Config
from db import db
from cdn import cdn, cdn_url

from models.food import (
    FoodInstructionsModel,
    FoodModel,
    FoodIngredientsModel
)
from models.allergy import (
    AllergyModel,
)

import os.path as op
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import *
from jinja2 import Markup

# Custom Image Upload
from wtforms import ValidationError
from wtforms.widgets import html_params
from flask_admin._compat import string_types
from io import BytesIO
import base64
try:
    from PIL import Image
except ImportError:
    Image = None

class AllergyModelAdmin(ModelView):
    column_searchable_list = ('name',)

    def __init__(self):
        super(AllergyModelAdmin, self).__init__(AllergyModel, db.session, name='Allergy')

class CustomImageUploadInput(object):
    empty_template = ('<input %(file)s>')
    data_template = ('<div class="image">'
                     ' <img %(image)s>'
                     ' <input type="checkbox" name="%(marker)s">Delete</input>'
                     ' <input %(text)s>'
                     '</div>'
                     '<input %(file)s>')

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)

        args = {
            'text': html_params(type='hidden',
                                value=field.data,
                                name=field.name),
            'file': html_params(type='file',
                                **kwargs),
            'marker': '_%s-delete' % field.name
        }

        if field.data and isinstance(field.data, string_types):
            url = self.get_url(field)
            args['image'] = html_params(src=url)

            template = self.data_template
        else:
            template = self.empty_template

        return Markup(template % args)

    def get_url(self, field):
        return cdn_url('food',field.data)

class CustomImageUploadField(FileUploadField):
    widget = CustomImageUploadInput()

    def __init__(self, label=None, allowed_extensions=None,
                 max_size=None,
                 namegen=None,
                 **kwargs):
 
        if Image is None:
            raise ImportError('PIL library was not found')

        self.max_size = max_size
        self.image = None

        if not allowed_extensions:
            allowed_extensions = ('jpg', 'jpeg', 'png', 'tiff', 'jfif')

        super(CustomImageUploadField, self).__init__(label,
                                               allowed_extensions=allowed_extensions,
                                               namegen=namegen,
                                               **kwargs)


    def pre_validate(self, form):
        super(CustomImageUploadField, self).pre_validate(form)
        if self._is_uploaded_file(self.data):
            try:
                self.image = Image.open(self.data)
            except Exception as e:
                raise ValidationError('Invalid image: %s' % e)

    # Deletion
    def _delete_file(self, filename):
        list_files = cdn.list_files({"name": filename})
        try : 
            fileId = list_files['response'][0]['fileId']
            cdn.delete_file(fileId)
        except Exception as e:
            pass
        
    # Saving
    def _save_file(self, data, filename):

        # Figure out format
        filename, format = self._get_save_format(filename, self.image)

        if self.image and self.max_size:
            if self.max_size:
                image = self._resize(self.image, self.max_size)
            else:
                image = self.image
        else:
            data.seek(0)
            data.save(self._get_path(filename))
            image = data

        return self._save_image(image, filename, format)

    def _resize(self, image, size):
        (width, height) = size
        if image.size[0] > width or image.size[1] > height:
            thumb = self.image.copy()
            thumb.thumbnail((width, height), Image.ANTIALIAS)
            return thumb
        return image

    def _save_image(self, image, filename, format='JPEG'):
        try:
            if image.mode not in ('RGB', 'RGBA'):
                image = image.convert('RGBA')
        except Exception as e:
            pass

        buffered  = BytesIO()
        image.save(buffered, format)
        img_str = base64.b64encode(buffered.getvalue())
        upload = cdn.upload_file(
            file= img_str, # required
            file_name= filename, # required
            options= {
                "folder" : "/food_image/",
                "is_private_file": False,
                "use_unique_file_name": True,
                "response_fields": ["file_name"],
            }
        )
        filename = upload['response']['name']
        return filename

    def _get_save_format(self, filename, image):
        name, ext = op.splitext(filename)
        return name, image.format

class FoodModelAdmin(ModelView):
    column_searchable_list = ('name',)
    column_list = ('id','name','food_type','duration','serving','difficulty','tags','image_filename','calorie','protein','fat','carbohydrate','fiber','calcium','phosphor','iron','sodium','potassium','copper','zinc','vit_a','vit_b1','vit_b2','vit_b3','vit_c')

    def _list_thumbnail(view, context, model, name):
        if not model.image_filename:
            return ''

        return Markup(
            '<img src="%s" style="max-height:200px;">' %
            cdn_url('food',model.image_filename)
        )

    def food_name(obj, file_data):
        return obj.name


    column_formatters = {
        'image_filename': _list_thumbnail
    }

    form_extra_fields = {
        'image_filename': CustomImageUploadField(
            'Image',max_size=(500,500),namegen=food_name)
    }


    form_columns = ('name','food_type','duration','serving','difficulty','tags','image_filename')
    inline_models = (FoodInstructionsModel,)

    create_template = 'food/admin_add_food_interface.html'
    def __init__(self):
        super(FoodModelAdmin, self).__init__(FoodModel, db.session, name='Food')

class FoodIngredientsModelAdmin(ModelView):
    form_excluded_columns = ('foods',)
    column_searchable_list = ('name',)

    def __init__(self):
        super(FoodIngredientsModelAdmin, self).__init__(FoodIngredientsModel, db.session, name='Ingredients')



