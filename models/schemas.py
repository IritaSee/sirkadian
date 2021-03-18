from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow_enum import EnumField
import enum
from db import db
from ma import ma
from marshmallow import fields
from models.user import UserModel
from models.enum import (
    FoodType
)
from models.food import (
    FoodModel,
    FoodIngredientsModel,
    FoodAnalyticsModel,
    FoodIngredientsInfoModel,
    FoodInstructionsModel,
    FoodHelperModel,
    FoodMaxModel
)
from models.user_history import (
    UserFoodHistoryModel
)
from models.tags import (
    TagsModel
)

from models.allergy import *

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

class FoodIngredientsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FoodIngredientsModel

class FoodIngredientsInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FoodIngredientsInfoModel

class FoodInstructionsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FoodInstructionsModel

class FoodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FoodModel
    food_ingredients = ma.Nested('FoodIngredientsSchema', only=('id', 'name'), many=True)
    food_ingredients_info = ma.Nested('FoodIngredientsInfoSchema', many=True)
    food_instructions = ma.Nested('FoodInstructionsSchema', many=True)

class FoodHelperSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FoodHelperModel

class FoodMaxSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FoodMaxModel

class FoodAnalyticsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FoodAnalyticsModel
    food = ma.Nested('FoodSchema', only=('id', 'name'))

class UserFoodHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserFoodHistoryModel
    user = ma.Nested('UserSchema', only=('id', 'name'), many=True)
    food = ma.Nested('FoodSchema', only=('id', 'name'), many=True)

class TagsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TagsModel

class AllergySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AllergyModel
    ingredients = ma.Nested('FoodIngredientsSchema', only=('id', 'name'), many=True)