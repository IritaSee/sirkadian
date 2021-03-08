from db import db

import json

class AllergyModel(db.Model):
    __tablename__ = 'allergy'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(80), nullable=False)
    ingredients = db.relationship(
        'FoodIngredientsModel',
        secondary=allergy_ingredients_assoc,
        backref="allergy_ingredients",
        lazy='joined'
    )
    
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