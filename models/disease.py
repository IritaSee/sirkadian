from db import db
from models.enum import (
    organ_system,
)
from models.food import (
    FoodModel
)
from models.sport import (
    SportModel
)

class DiseaseModel(db.Model):
    __tablename__ = 'disease'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(80), nullable=False)
    organ_system = db.Column('organ_system', db.Enum(organ_system))
    food_prohibition = db.Column('food_prohibition', db.Integer, db.ForeignKey(FoodModel.id))
    sport_prohibition = db.Column('sport_prohibition', db.Integer, db.ForeignKey(SportModel.id))

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
    def find_by_organ_system(cls, val):
        return cls.query.filter_by(organ_system=val).all()

    @classmethod
    def find_by_food_prohibition(cls, val):
        return cls.query.filter_by(food_prohibition=val).all()

    @classmethod
    def find_by_sport_prohibition(cls, val):
        return cls.query.filter_by(sport_prohibition=val).all()