from flask import request
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from models.user import UserModel
from models.user_history import (
    UserLoginHistoryModel
)
from blacklist import BLACKLIST
from models.enum import (
    user_gender,
    user_lang
)
import datetime

class UserRegister(Resource):
    def post(self):
        data = request.get_json(force=True)

        if UserModel.find_by_username(data['username']):
            return {"message": "Username taken"}, 400

        d, m, y = data['dob'].split('-') # dd-mm-yyyy
        dob_to_input = datetime.datetime(int(y), int(m), int(d))

        try:
            if data['gender'] == 'male':
                gender_to_input = user_gender.MALE
            elif data['gender'] == 'female':
                gender_to_input = user_gender.FEMALE
        except Exception as e:
            return {"message": e}, 200
            
        try:
            if data['lang'] == 'eng':
                lang_to_input = user_lang.ENG
            elif data['lang'] == 'idn':
                lang_to_input = user_lang.IDN
        except Exception as e:
            return {"message": e}, 200

        try:
            if data['password']:
                password_to_input = generate_password_hash(data['password'])
        except Exception as e:
            return {"message": e}, 200

        data_to_input = UserModel(
            username=data['username'],
            password=password_to_input,
            dob=dob_to_input,
            email=data['email'],
            gender=gender_to_input,
            lang=lang_to_input,
            ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
        )

        data_to_input.save_to_db()

        return {
            "message": "Success!",
            "username": data['username'],
            "activated": 0
        }, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200

class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = request.get_json(force=True)
        user = UserModel.find_by_username(data['username'])
        # if user.activated == False return message error
        if user and check_password_hash(user.password, data['password']) and user.activated == 1:
            token = create_access_token(identity=user.id, fresh=True)
            history_to_input = UserLoginHistoryModel(
                user_id=user.id,
                token=token,
                ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            )
            history_to_input.save_to_db()
            return {
                'user_id': user.id,
                'username': data['username'],
                'email': user.email,
                'token': token,
            }, 200
        return {'message': 'Invalid credentials'}, 401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out'}, 200

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200

# class UserActivation:
# ambil kode dari input json
# cek di database
# set activated=True atau False jika no match

# class UserInitialSetup:
# cek di database ada user id atau tidak
# cek di db activated=True
# get json
# set to new var json[ttl], json[gender], json[lang], json[tb], json[bb], json[tingkat keaktifan], json[preferensi olga], json[veget], json[maintain_weight]
# update db where user_id = user.id values ttl, gender, lang
# insert user_health_history values user_Id, tb, bb, tingkat keaktifan, preferensi olga, veget, maintain_weight
# insert user_allergy_history values user_ID, allergy (satu entry per row)
# insert user_disease_history values user_ID, disease (satu entry per row)
# insert user_addiction_history values user_ID, addiction (satu entry per row)
# DELETE data yg dimasukin kesini dari class UserRegister

#class UserForgotPasswordInit:
# if POST:
# if email is in db, get user id, make random number 6 digits, insert user_id, code, created_at to table user_forgot_password
# hash code
# send email with hashed code

#class UserForgotPasswordVerify:
# if request = sirkadian.com/forgot_password?id=30&code=hashedcode
# if POST:
# get user id, unhash code posted, check if == unhashed code user_forgot_password where user_id

# class UserChangePassword:
# check if last entry of user id in user_forgot_password table < 1 jam
# UserModel.find by id, make new model  with new password, update entry at user table
# return success message

