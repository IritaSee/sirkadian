from db import db
from models.enum import (
    user_gender,
    user_lang
)

# defining models
class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(80), unique=True)
    password = db.Column('password', db.Text)
    dob = db.Column('dob', db.Date)
    email = db.Column('email', db.String(150), unique=True)
    gender = db.Column('gender', db.String(5))
    lang = db.Column('lang', db.Enum(user_lang))
    activated = db.Column('activated', db.Boolean, default=False)
    ip_address = db.Column('ip_address', db.String(18))
    is_admin = db.Column('is_admin', db.Boolean, default=False)
    created_at = db.Column('created_at', db.DateTime, default=db.func.now(), nullable=False)

    def __init__(
            self,
            username,
            password,
            dob,
            email,
            gender,
            lang,
            activated,
            ip_address
        ):
        self.username = username
        self.password = password
        self.dob = dob
        self.email = email
        self.gender = gender
        self.lang = lang
        self.activated = activated
        self.ip_address = ip_address

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'dob': self.dob,
            'email': self.email,
            'gender': self.gender,
            'lang': self.lang,
            'login_retry': self.login_retry,
            'last_retry': self.last_retry,
            'activated': self.activated,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

class UserVerificationModel(db.Model):
    __tablename__ = 'users_verification'
    
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    code = db.Column('code', db.String(100), nullable=False)
    purpose = db.Column('purpose', db.String(100), nullable=False) # register, forgotpass
    ip_address = db.Column('ip_address', db.String(18))
    created_at = db.Column('created_at', db.DateTime, default=db.func.now(), nullable=False)

    def __init__(
            self,
            user_id,
            code,
            ip_address
        ):
        self.user_id = user_id
        self.code = code
        self.ip_address = ip_address

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'code': self.code
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_user_id(cls, _id):
        return cls.query.filter_by(user_id=_id).first()
