from config import Config
from db import db
from flask_admin import form
from flask_admin.contrib.sqla import ModelView

from models.food import (
    FoodInstructionsModel,
    FoodModel,
    FoodIngredientsModel
)
from models.allergy import (
    AllergyModel,
)

from jinja2 import Markup
from flask import url_for

class AllergyModelAdmin(ModelView):
    column_searchable_list = ('name',)

    def __init__(self):
        super(AllergyModelAdmin, self).__init__(AllergyModel, db.session, name='Allergy')


class FoodModelAdmin(ModelView):
    # form_columns = ('name','food_type','duration','serving','difficulty','tags','image_filename')
    # column_list = ('name','food_type','duration','serving','difficulty','tags','image_filename')
    column_searchable_list = ('name',)
    column_list = ('id','name','food_type','duration','serving','difficulty','tags','image_filename','calorie','protein','fat','carbohydrate','fiber','calcium','phosphor','iron','sodium','potassium','copper','zinc','vit_a','vit_b1','vit_b2','vit_b3','vit_c')
    # column_exclude_list = ('serving','image_filename','rating','nutri_point')

    def _list_thumbnail(view, context, model, name):
        if not model.image_filename:
            return ''

        return Markup(
            '<img src="%s" width="200" height="auto">' %
            url_for('send_file',filename='food_image/%s'%model.image_filename)
        )

    column_formatters = {
        'image_filename': _list_thumbnail
    }

    form_extra_fields = {
        'image_filename': form.ImageUploadField(
            'Image',endpoint='send_file',url_relative_path="food_image/",base_path=Config.FILE_PATH)
    }


    form_columns = ('name','food_type','duration','serving','difficulty','tags','image_filename')
                # 'Image', base_path=file_path, thumbnail_size=(100, 100, True))
    inline_models = (FoodInstructionsModel,)

    create_template = 'food/admin_add_food_interface.html'
    def __init__(self):
        super(FoodModelAdmin, self).__init__(FoodModel, db.session, name='Food')

class FoodIngredientsModelAdmin(ModelView):
    # form_columns = ('name','food_type','duration','difficulty','tags',)
    form_excluded_columns = ('foods',)
    column_searchable_list = ('name',)
    # column_exclude_list = ('serving','image_filename','rating','nutri_point')

    # inline_models = (FoodInstructionsModel,)

    # create_template = 'food/admin_add_food_interface.html'
    def __init__(self):
        super(FoodIngredientsModelAdmin, self).__init__(FoodIngredientsModel, db.session, name='Ingredients')



