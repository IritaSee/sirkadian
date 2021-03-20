from db import db
from cdn import cdn_url
from models.assoc import (
    food_ingredients_assoc,
    food_ingredients_info_assoc,
    food_instructions_assoc,
    trending_food_assoc
)
import json
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func

class FoodIngredientsModel(db.Model):
    __tablename__ = 'food_ingredients'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(80), nullable=False)
    # recipe = db.relationship('FoodRecipeModel', secondary=food_recipe_ingredients_assoc, backref=db.backref('food_user_recipe'), lazy=True)
    calorie = db.Column('calorie', db.Float) # kal
    protein = db.Column('protein', db.Float) # gram
    fat  = db.Column('fat', db.Float) # gram
    carbohydrate = db.Column('carbohydrate', db.Float) # gram
    fiber = db.Column('fiber', db.Float) # gram
    calcium = db.Column('calcium', db.Float) # miligram
    phosphor = db.Column('phosphor', db.Float) # miligram
    iron = db.Column('iron', db.Float) # miligram
    sodium = db.Column('sodium', db.Float) # miligram
    potassium = db.Column('potassium', db.Float) # miligram
    copper = db.Column('copper', db.Float) # miligram
    zinc = db.Column('zinc', db.Float) # miligram
    vit_a = db.Column('vit_a', db.Float) # mcg
    vit_b1 = db.Column('vit_b1', db.Float) # vit b1, miligram
    vit_b2 = db.Column('vit_b2', db.Float) # vit b2, miligram
    vit_b3 = db.Column('vit_b3', db.Float) # vit b3, miligram
    vit_c = db.Column('vit_c', db.Float) # miligram
    ing_type = db.Column('ing_type', db.String(20)) # mentah/olahan
    food_group = db.Column('food_group', db.String(20)) # buah/sayur/bumbu/dsb

    def __repr__(self):
        return self.name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'calorie' : self.calorie,
            'protein' : self.protein,
            'fat' : self.fat,
            'carbohydrate' : self.carbohydrate,
            'fiber' : self.fiber,
            'calcium' : self.calcium,
            'phosphor' : self.phosphor,
            'iron' : self.iron,
            'sodium' : self.sodium,
            'potassium' : self.potassium,
            'copper' : self.copper,
            'zinc' : self.zinc,
            'vit_a' : self.vit_a,
            'b_carotene' : self.b_carotene,
            'carotene_total' : self.carotene_total,
            'vit_b1' : self.vit_b1,
            'vit_b2' : self.vit_b2,
            'vit_b3' : self.vit_b3,
            'vit_c' : self.vit_c,
            'ing_type' : self.ing_type,
            'food_group' : self.food_group
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_food_type(cls, val):
        return cls.query.filter_by(food_type=val).all()

    @classmethod
    def find_by_calorie(cls, val):
        return cls.query.filter(cls.calorie <= val).all()

    @classmethod
    def find_all_id_name(cls):
        return cls.query.with_entities(
            FoodIngredientsModel.id,
            FoodIngredientsModel.name
        ).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

class FoodIngredientsInfoModel(db.Model):
    __tablename__ = 'food_ingredients_info'

    id = db.Column('id', db.Integer, primary_key=True)
    ingredients_info = db.Column('ingredients_info', db.Text)

    def __repr__(self):
        return self.ingredients_info

    def json(self):
        return {
            'id': self.id,
            'ingredients_info': self.ingredients_info
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_food_type(cls, val):
        return cls.query.filter_by(food_type=val).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

class FoodInstructionsModel(db.Model):
    __tablename__ = 'food_instructions'

    id = db.Column('id', db.Integer, primary_key=True)
    instructions = db.Column('instructions', db.Text)

    def json(self):
        return {
            'id': self.id,
            'instructions' : self.instructions
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_food_type(cls, val):
        return cls.query.filter_by(food_type=val).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

class FoodModel(db.Model):
    __tablename__ = 'food'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(80), nullable=False)
    food_type = db.Column('food_type', db.String(50))
    food_ingredients = db.Column('food_ingredients', db.Text)
    food_ingredients = db.relationship(
        'FoodIngredientsModel',
        secondary=food_ingredients_assoc,
        backref="foods",
        lazy='joined'
    )
    food_ingredients_info = db.relationship(
        'FoodIngredientsInfoModel',
        secondary=food_ingredients_info_assoc,
        backref="foods_ing_info",
        lazy='joined',
        uselist=True
    )
    food_instructions = db.relationship(
        'FoodInstructionsModel',
        secondary=food_instructions_assoc,
        backref="foods_ins",
        lazy='joined',
        uselist=True
    )
    duration = db.Column('duration', db.Integer) #durasi memasak, dihitung dlm detik
    serving = db.Column('serving', db.Integer) # integer, berapa porsi
    difficulty = db.Column('difficulty', db.String(20)) # easy, medium, hard
    calorie = db.Column('calorie', db.Float) # kal
    protein = db.Column('protein', db.Float) # gram
    fat  = db.Column('fat', db.Float) # gram
    carbohydrate = db.Column('carbohydrate', db.Float) # gram
    fiber = db.Column('fiber', db.Float) # gram
    calcium = db.Column('calcium', db.Float) # miligram
    phosphor = db.Column('phosphor', db.Float) # miligram
    iron = db.Column('iron', db.Float) # miligram
    sodium = db.Column('sodium', db.Float) # miligram
    potassium = db.Column('potassium', db.Float) # miligram
    copper = db.Column('copper', db.Float) # miligram
    zinc = db.Column('zinc', db.Float) # miligram
    vit_a = db.Column('vit_a', db.Float) # mcg
    vit_b1 = db.Column('vit_b1', db.Float) # vit b1, miligram
    vit_b2 = db.Column('vit_b2', db.Float) # vit b2, miligram
    vit_b3 = db.Column('vit_b3', db.Float) # vit b3, miligram
    vit_c = db.Column('vit_c', db.Float) # miligram
    rating = db.Column('rating', db.Integer)
    tags = db.Column('tags', db.Text)
    image_filename = db.Column('image_filename', db.Text)
    nutri_point = db.Column('nutri_point', db.Float)

    def image_url(self):
        return cdn_url('food',self.image_filename)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_food_type(cls, val):
        return cls.query.filter_by(food_type=val).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def get_nutrients(cls, _id):
        pass

class FoodHelperModel(db.Model):
    __tablename__ = 'food_helper'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(80), nullable=False)
    food_type = db.Column('food_type', db.String(10))
    duration = db.Column('duration', db.Integer) #durasi memasak, dihitung dlm detik
    serving = db.Column('serving', db.Integer) # integer, berapa porsi
    difficulty = db.Column('difficulty', db.String(20)) # easy, medium, hard
    calorie = db.Column('calorie', db.Float) # kal
    protein = db.Column('protein', db.Float) # gram
    fat  = db.Column('fat', db.Float) # gram
    carbohydrate = db.Column('carbohydrate', db.Float) # gram
    fiber = db.Column('fiber', db.Float) # gram
    calcium = db.Column('calcium', db.Float) # miligram
    phosphor = db.Column('phosphor', db.Float) # miligram
    iron = db.Column('iron', db.Float) # miligram
    sodium = db.Column('sodium', db.Float) # miligram
    potassium = db.Column('potassium', db.Float) # miligram
    copper = db.Column('copper', db.Float) # miligram
    zinc = db.Column('zinc', db.Float) # miligram
    vit_a = db.Column('vit_a', db.Float) # mcg
    vit_b1 = db.Column('vit_b1', db.Float) # vit b1, miligram
    vit_b2 = db.Column('vit_b2', db.Float) # vit b2, miligram
    vit_b3 = db.Column('vit_b3', db.Float) # vit b3, miligram
    vit_c = db.Column('vit_c', db.Float) # miligram
    tags = db.Column('tags', db.Text)
    image_filename = db.Column('image_filename', db.Text)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'food_type' : self.food_type,
            # 'food_ingredients' : self.food_ingredients,
            # 'food_ingredient_instructions' : self.food_ingredient_instructions,
            # 'food_instructions' : self.food_instructions,
            'serving' : self.serving,
            'difficulty' : self.difficulty,
            'calorie' : self.calorie,
            'protein' : self.protein,
            'fat' : self.fat,
            'carbohydrate' : self.carbohydrate,
            'fiber' : self.fiber,
            'calcium' : self.calcium,
            'phosphor' : self.phosphor,
            'iron' : self.iron,
            'sodium' : self.sodium,
            'potassium' : self.potassium,
            'copper' : self.copper,
            'zinc' : self.zinc,
            'vit_a' : self.vit_a,
            'vit_b1' : self.vit_b1,
            'vit_b2' : self.vit_b2,
            'vit_b3' : self.vit_b3,
            'vit_c' : self.vit_c,
            'tags' : self.tags,
            'image_filename' : self.image_filename
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_food_type(cls, val):
        return cls.query.filter_by(food_type=val).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def get_nutrients(cls, _id):
        pass

class FoodMaxModel(db.Model):
    __tablename__ = 'food_max'

    id = db.Column('id', db.Integer, primary_key=True)
    max_calorie = db.Column('max_calorie', db.Float) # kal
    max_protein = db.Column('max_protein', db.Float) # gram
    max_fat  = db.Column('max_fat', db.Float) # gram
    max_carbohydrate = db.Column('max_carbohydrate', db.Float) # gram
    max_fiber = db.Column('max_fiber', db.Float) # gram
    max_calcium = db.Column('max_calcium', db.Float) # miligram
    max_phosphor = db.Column('max_phosphor', db.Float) # miligram
    max_iron = db.Column('max_iron', db.Float) # miligram
    max_sodium = db.Column('max_sodium', db.Float) # miligram
    max_potassium = db.Column('max_potassium', db.Float) # miligram
    max_copper = db.Column('max_copper', db.Float) # miligram
    max_zinc = db.Column('max_zinc', db.Float) # miligram
    max_vit_a = db.Column('max_vit_a', db.Float) # mcg
    max_vit_b1 = db.Column('max_vit_b1', db.Float) # vit b1, miligram
    max_vit_b2 = db.Column('max_vit_b2', db.Float) # vit b2, miligram
    max_vit_b3 = db.Column('max_vit_b3', db.Float) # vit b3, miligram
    max_vit_c = db.Column('max_vit_c', db.Float) # miligram

class FoodRecipeIngredientsModel(db.Model):
    __tablename__ = 'food_recipe'

    id = db.Column('id', db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    food_ingredients_id = db.Column(db.Integer, db.ForeignKey('food_ingredients.id'), nullable=False) #db.relationship('FoodIngredientsModel', secondary=food_recipe_ingredients_assoc, backref=db.backref('food_user_recipe_ingredients'), lazy=True)
    ingredients_amt = db.Column('ingredients_amt', db.Integer())
    ingredients_unit = db.Column('ingredients_unit', db.String(50))
    ingredients_info = db.Column('ingredients_info', db.String(100))

    def json(self):
        return {
            'id': self.id,
            'food_id': self.food_id,
            'food_ingredients_id' : self.food_ingredients_id,
            'ingredients_amt': self.ingredients_amt,
            'ingredients_unit': self.ingredients_unit,
            'ingredients_info' : self.ingredients_info
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

class FoodAnalyticsModel(db.Model):
    __tablename__ = 'analytics_food'

    id = db.Column('id', db.Integer, primary_key=True)
    food_id = db.Column('food', db.Integer, db.ForeignKey('food.id'))
    food = db.relationship('FoodModel')
    ip_address = db.Column('ip_address', db.String(18))
    created_at = db.Column('created_at', db.DateTime, default=db.func.now(), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'food_id': self.food_id,
            'created_at': self.created_at
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(food_id=_id).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

class FoodRatingModel(db.Model):
    __tablename__ = 'food_rating'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user', db.Integer, db.ForeignKey('users.id'))
    food_id = db.Column('food', db.Integer, db.ForeignKey('food.id'))
    rating = db.Column('rating', db.Integer)
    ip_address = db.Column('ip_address', db.String(18))
    created_at = db.Column('created_at', db.DateTime, default=db.func.now(), nullable=False)