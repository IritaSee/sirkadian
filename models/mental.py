from db import db
from models.enum import (
    song_mood
)

import json

class MeditationModel(db.Model):
    __tablename__ = 'meditation'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(80), nullable=False)
    duration = db.Column('duration', db.Integer)
    link = db.Column('link', db.String(120))

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
    def find_by_duration(cls, duration):
        return cls.query.filter(cls.duration <= duration).all()

class SongModel(db.Model):
    __tablename__ = 'song'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(80), nullable=False)
    mood = db.Column('mood', db.Enum(song_mood))
    duration = db.Column('duration', db.Integer)
    link = db.Column('link', db.String(120))

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
    def find_by_duration(cls, duration):
        return cls.query.filter(cls.duration <= duration).all()

    @classmethod
    def find_by_mood(cls, mood):
        return cls.query.filter_by(mood=mood).all()