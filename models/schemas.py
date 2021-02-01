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
    FoodAnalyticsModel
)
from models.user_history import (
    UserFoodHistoryModel
)
from models.tags import (
    TagsModel
)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

class FoodIngredientsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FoodIngredientsModel

class FoodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FoodModel
    food_ingredients = ma.Nested('FoodIngredientsSchema', only=('id', 'name'), many=True)

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