from db import db
from models.enum import (
    organ_system,
    sport_difficulty
)

class SportModel(db.Model):
    __tablename__ = 'sport'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(80), nullable=False)
    cps = db.Column('cps', db.Float)
    difficulty = db.Column('difficulty', db.Enum(sport_difficulty))
    amount = db.Column('amount', db.Integer)
    sets = db.Column('sets', db.Integer)
    duration = db.Column('duration', db.Integer) # estimated duration per set

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
    def find_by_cps(cls, val):
        return cls.query.filter(cls.cps <= val).all()

    @classmethod
    def find_by_difficulty(cls, difficulty):
        return cls.query.filter_by(difficulty=difficulty).all()

    @classmethod
    def find_by_duration(cls, duration):
        return cls.query.filter(cls.duration <= duration).all()