from db import db

from models.enum import (
    activity_level,
    sport_difficulty,
    food_type,
    mood_state,
    organ_system,
    song_mood
)

from models.user import UserModel
from models.assoc import *
from models.food import *
from models.sport import *
from models.disease import *
from models.addiction import *
from models.allergy import *
from models.mental import *

class UserLoginHistoryModel(db.Model):
    __tablename__ = 'user_login_history'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    jti_access = db.Column(db.String(36), nullable=False)
    jti_refresh = db.Column(db.String(36), nullable=False)
    revoked = db.Column('revoked', db.Boolean)
    expires = db.Column(db.DateTime, nullable=False)
    ip_address = db.Column('ip_address', db.String(18))
    created_at = db.Column('created_at', db.DateTime, default=db.func.now())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(user_id=_id).first()

class UserHealthHistoryModel(db.Model):
    __tablename__ = 'user_health_history'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    height = db.Column('height', db.Float) # cm
    weight = db.Column('weight', db.Float) # kg
    activity_level = db.Column('activity_level', db.String(10)) # sedentary, low, medium, high
    vegan = db.Column('vegan', db.Boolean)
    maintain_weight = db.Column('maintain_weight', db.Integer) # 0=maintain, 1= lose slow, 2= lose medium, 3= lose fast, 4=gain slow, 5=gain medium, 6=gain fast
    sport_difficulty = db.Column('sport_difficulty', db.String(8)) # easy, medium, hard
    ip_address = db.Column('ip_address', db.String(18))
    created_at = db.Column('created_at', db.DateTime, default=db.func.now())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(user_id=_id).first()

class UserFoodHistoryModel(db.Model):
    __tablename__ = 'user_food_history'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    food = db.relationship(
        'FoodModel',
        secondary=food_history_assoc,
        backref='food_user_history',
        lazy='joined'
    )
    food_type = db.Column('food_type', db.String(30))
    total_calorie = db.Column('total_calorie', db.Float)
    ip_address = db.Column('ip_address', db.String(18))
    created_at = db.Column('created_at', db.DateTime, default=db.func.now())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(id=_id).all()

    @classmethod
    def find_food_by_user_id(cls, _id):
        return cls.query.with_entities(cls.food).filter_by(id=_id).all()

class UserSportHistoryModel(db.Model):
    __tablename__ = 'user_sport_history'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    sport = db.relationship(
        'SportModel',
        secondary=sport_history_assoc,
        backref='user_sport',
        lazy='joined'
    )
    ip_address = db.Column('ip_address', db.String(18))
    created_at = db.Column('created_at', db.DateTime, default=db.func.now())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(id=_id).all()

    @classmethod
    def find_sport_by_user_id(cls, _id):
        return cls.query.with_entities(cls.sport).filter_by(id=_id).all()

class UserDiseaseHistoryModel(db.Model):
    __tablename__ = 'user_disease_history'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    disease = db.relationship(
        'DiseaseModel',
        secondary=disease_history_assoc,
        backref='user_disease',
        lazy='joined'
    )
    disease_when = db.Column('disease_when', db.Date)
    ip_address = db.Column('ip_address', db.String(18))
    created_at = db.Column('created_at', db.DateTime, default=db.func.now())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(id=_id).all()

    @classmethod
    def find_disease_by_user_id(cls, _id):
        return cls.query.with_entities(cls.disease).filter_by(id=_id).all()

class UserAddictionHistoryModel(db.Model):
    __tablename__ = 'user_addiction_history'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    addiction = db.relationship(
        'AddictionModel',
        secondary=addiction_history_assoc,
        backref='user_addiction',
        lazy='joined'
    )
    addiction_when = db.Column('addiction_when', db.Date)
    ip_address = db.Column('ip_address', db.String(18))
    created_at = db.Column('created_at', db.DateTime, default=db.func.now())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(id=_id).all()

    @classmethod
    def find_addiction_by_user_id(cls, _id):
        return cls.query.with_entities(cls.addiction).filter_by(id=_id).all()

class UserAllergyHistoryModel(db.Model):
    __tablename__ = 'user_allergy_history'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    allergy = db.relationship(
        'AllergyModel',
        secondary=allergy_history_assoc,
        backref='user_allergy',
        lazy='joined'
    )
    allergy_when = db.Column('allergy_when', db.Date)
    ip_address = db.Column('ip_address', db.String(18))
    created_at = db.Column('created_at', db.DateTime, default=db.func.now())

    def __repr__(self):
        return str(self.user_id)
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(id=_id).all()

    @classmethod
    def find_alergy_by_user_id(cls, _id):
        return cls.query.with_entities(cls.allergy).filter_by(id=_id).all()

class UserSleepHistoryModel(db.Model):
    __tablename__ = 'user_sleep_history'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column('start_time', db.DateTime, default=db.func.now())
    start_date = db.Column('start_date', db.Date, default=db.func.now())
    ip_address = db.Column('ip_address', db.String(18))
    created_at = db.Column('created_at', db.DateTime, default=db.func.now())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(id=_id).all()

class UserMoodHistoryModel(db.Model):
    __tablename__ = 'user_mood_history'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood_state = db.Column('mood_state', db.Enum(mood_state))
    mood_when = db.Column('mood_when', db.DateTime, default=db.func.now())
    ip_address = db.Column('ip_address', db.String(18))
    created_at = db.Column('created_at', db.DateTime, default=db.func.now())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(id=_id).all()

class UserMeditationHistoryModel(db.Model):
    __tablename__ = 'user_meditation_history'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    meditation = db.relationship(
        'MeditationModel',
        secondary=meditation_history_assoc,
        backref='user_meditation',
        lazy='joined'
    )
    meditation_when = db.Column('meditation_when', db.DateTime, default=db.func.now())
    duration = db.Column('duration', db.Integer) #define duration as seconds
    ip_address = db.Column('ip_address', db.String(18))
    created_at = db.Column('created_at', db.DateTime, default=db.func.now())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(id=_id).all()

class UserSongHistoryModel(db.Model):
    __tablename__ = 'user_song_history'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    song = db.relationship(
        'SongModel',
        secondary=song_history_assoc,
        backref='user_song',
        lazy=True
    )
    song_when = db.Column('song_when', db.DateTime, default=db.func.now())
    duration = db.Column('duration', db.Integer) #define duration as seconds
    ip_address = db.Column('ip_address', db.String(18))
    created_at = db.Column('created_at', db.DateTime, default=db.func.now())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(id=_id).all()

    @classmethod
    def find_by_song_id(cls, _id):
        return cls.query.filter_by(song_id=_id).first()