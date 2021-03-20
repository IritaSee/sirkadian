from random import randint
from flask import request
from flask_restful import Resource, reqparse, Api
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
    decode_token
)
from db import db
from mail import mail
from flask_mail import Message
from models.user import (
    UserModel,
    UserVerificationModel
)
from models.addiction import AddictionModel
from models.allergy import AllergyModel
from models.disease import DiseaseModel
from models.user_history import (
    UserLoginHistoryModel,
    UserAddictionHistoryModel,
    UserAllergyHistoryModel,
    UserDiseaseHistoryModel,
    UserHealthHistoryModel
)
from blacklist import (
    _epoch_utc_to_datetime,
    is_token_revoked,
    revoke_token,
    prune_database
)
from models.enum import (
    user_gender,
    user_lang
)
import datetime

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

class UserRegister(Resource):
    def post(self):
        data = request.get_json(force=True)

        if UserModel.find_by_username(data['username']):
            return {"message": "Username taken"}, 400

        try:
            if data['password']:
                password_to_input = generate_password_hash(data['password'], 'sha256')
        except Exception as e:
            return {"message": e}, 400

        data_to_input = UserModel(
            username=data['username'],
            password=password_to_input,
            email=data['email'],
            ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        )

        try:
            data_to_input.save_to_db()
        except:
            return {"message": "Error database step 1!"}

        user_id = UserModel.query.filter_by(username=data['username']).with_entities(UserModel.id).first()
        key = None
        key = str(randint(100000, 999999))
        code = generate_password_hash(key, 'sha256')
        try:
            data_to_input_verification = UserVerificationModel(
                user_id = user_id,
                code = code,
                purpose = 'register',
                ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            )
            data_to_input_verification.save_to_db()
        except:
            return {"message": "Error database step 2!"}
        
        msg = Message('Verifikasi akun Sirkadianmu', sender = 'sirkadiancorporation@gmail.com', recipients = data['email'].split())
        msg.html = "<h3>Verifikasi akun Sirkadianmu</h3><br><p>Masukkan kode ini " + str(key) + " di aplikasi Sirkadian untuk mengaktifkan akun Anda.</p><br><p>Abaikan pesan ini jika tidak merasa mendaftar</p><br></p>Terima kasih</p><br><p>Regards, Sirkadian</p>"
        mail.send(msg)

        return {
            "message": "Success!",
            "id": user_id.id,
        }, 201

class UserInitialSetup(Resource):
    @jwt_required
    def post(cls):
        data = request.get_json(force=True)
        user = UserModel.find_by_id(data['id'])
        user_id_token = get_jwt_identity()

        if user.id == user_id_token:
            if user.activated == True:
                d, m, y = data['dob'].split('-') # dd-mm-yyyy
                user.dob = datetime.datetime(int(y), int(m), int(d))

                exists_health_history = UserHealthHistoryModel.query.filter_by(user_id=user.id).first()
                if not exists_health_history :
                    data_to_input_health = UserHealthHistoryModel(
                        user_id = user.id,
                        height = data['height'],
                        weight = data['weight'],
                        activity_level = data['activity_level'],
                        sport_difficulty = data['sport_difficulty'],
                        vegan = data['vegan'],
                        ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                        maintain_weight = data['maintain_weight']
                    )
                    db.session.add(data_to_input_health)
                else :
                    exists_health_history.height = data['height']
                    exists_health_history.weight = data['weight']
                    exists_health_history.activity_level = data['activity_level']
                    exists_health_history.sport_difficulty = data['sport_difficulty']
                    exists_health_history.vegan = data['vegan']
                    exists_health_history.ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                    exists_health_history.maintain_weight = data['maintain_weight']

                allergy_dict = data['allergy']
                exists_allergy_history = UserAllergyHistoryModel.query.filter_by(user_id=user.id).first()
                if not exists_allergy_history :
                    data_to_input_allergy = UserAllergyHistoryModel(
                        user_id = user.id,
                        ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                    )
                    for item in allergy_dict:
                        data_to_input_allergy.allergy.append(AllergyModel.find_by_id(item))
                    db.session.add(data_to_input_allergy)
                else :
                    exists_allergy_history.ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                    exists_allergy_history.allergy = []
                    for item in allergy_dict:
                        exists_allergy_history.allergy.append(AllergyModel.find_by_id(item))
                
                disease_dict = data['disease']
                exists_disease_history = UserDiseaseHistoryModel.query.filter_by(user_id=user.id).first()
                if not exists_disease_history :
                    data_to_input_disease = UserDiseaseHistoryModel(
                        user_id = user.id,
                        ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                    )
                    for item in disease_dict:
                        data_to_input_disease.disease.append(DiseaseModel.find_by_id(item))
                    db.session.add(data_to_input_disease)
                else :
                    exists_disease_history.ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                    exists_disease_history.disease = []
                    for item in disease_dict:
                        exists_disease_history.disease.append(DiseaseModel.find_by_id(item))

                addiction_dict = data['addiction']
                exists_addiction_history = UserAddictionHistoryModel.query.filter_by(user_id=user.id).first()
                if not exists_addiction_history :
                    data_to_input_addiction = UserAddictionHistoryModel(
                        user_id = user.id,
                        ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                    )
                    for item in addiction_dict:
                        data_to_input_addiction.addiction.append(AddictionModel.find_by_id(item))
                    db.session.add(data_to_input_addiction)
                else :
                    exists_addiction_history.ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                    exists_addiction_history.addiction = []
                    for item in addiction_dict:
                        exists_addiction_history.addiction.append(AddictionModel.find_by_id(item))

                
                try :
                    db.session.commit()
                except:
                    db.session.rollback()
                    return {
                        'message': 'Database Error'
                    }

                return {
                    'message': 'Success, welcome to app!'
                }

            elif user['activated'] == False:
                return {
                    'message': 'Please activate first!'
                }
        elif not user.id == user_id_token:
            return {
                'message': 'Wrong token'
            }
        else:
            return {
                'message': 'Server error'
            }

def GenerateToken(id):
    access_token = create_access_token(identity=id, fresh=True)
    refresh_token = create_refresh_token(identity=id)
    decoded_access_token = decode_token(access_token)
    decoded_refresh_token = decode_token(refresh_token)
    expires = _epoch_utc_to_datetime(decoded_refresh_token['exp'])
    history_to_input = UserLoginHistoryModel(
        user_id = id,
        jti_access = decoded_access_token['jti'],
        jti_refresh = decoded_refresh_token['jti'],
        revoked = False,
        expires = expires,
        ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    )
    db.session.add(history_to_input)

    try :
        db.session.commit()
    except :
        return {'message': 'Database Error'}, 500
        
    return {
        'message': 'Success',
        'user_id': id,
        'access_token': access_token,
        'refresh_token': refresh_token
    }, 200

class UserActivation(Resource):
    @classmethod
    def post(cls):
        # ?id=....&code=.....
        _id = request.args.get('id')
        code = request.args.get('code')

        verification = UserVerificationModel.query.filter_by(user_id=_id, purpose='register').order_by(UserVerificationModel.id.desc()).first()
        if verification.used == False:
            if check_password_hash(verification.code, code) == True:
                user = UserModel.find_by_id(_id)
                user.activated = 1
                verification.used = True
                db.session.commit()
                
                # Auto Login
                return GenerateToken(user.id)
            else :
                return {'message': 'Wrong verification code!'}
        elif not verification.used == False:
            return {
                'message': 'Verification code already used'
            }
        elif not verification:
            return {
                'message': 'No data found with that user id'
            }
        else:
            return {
                'message': 'Server error..'
            }

class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = request.get_json(force=True)
        user = UserModel.find_by_username(data['username'])
        if user and check_password_hash(user.password, data['password']) and user.activated == 1:
            return GenerateToken(user.id)
        return {'message': 'Invalid credentials'}, 401

class UserLogout(Resource):
    @jwt_refresh_token_required
    def post(self):
        user_identity = get_jwt_identity()
        try:
            revoke_token(user_identity)
            return {'message': 'Token revoked'}, 200
        except:
            return {'message': 'The specified token was not found'}, 404

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200

class UserForgotPassword(Resource):
    @classmethod
    def post(cls, option):
        if option == 1: # User Forgot Password Init
            data = request.get_json(force=True) #{ 'identity': 'aurelius@vito' or 'auvito' }
            user = UserModel.find_by_email(data['identity']) or UserModel.find_by_username(data['identity'])
            if user:
                key = str(randint(100000, 999999))
                code = generate_password_hash(key, 'sha256')
                data_to_input_verification = UserVerificationModel(
                    user_id = user.id,
                    code = code,
                    purpose = 'forgotpass',
                    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                )
                data_to_input_verification.save_to_db()

                msg = Message('Sirkadian Lupa Password', sender = 'sirkadiancorporation@gmail.com', recipients = [user.email])
                msg.html = "<h3>Lupa Password Sirkadian</h3><br><p>Klik link <a href='sirkadian.com/forgot_password?id=" + str(user.id) + "&code=" + str(key) + "'>ini untuk mengatur ulang password Anda.</a><br><p>Abaikan pesan ini jika tidak merasa lupa password</p><br></p>Terima kasih</p><br><p>Regards, Sirkadian</p>"
                mail.send(msg)

                return {
                    'message': 'Success! Silahkan cek email Anda'
                }
            else:
                return {
                    'message': 'User tidak ditemukan'
                }
        elif option == 2: # User Change Password
            data = request.get_json(force=True)
            new_password = data['new_password']
            _id = data['user_id']

            verification = UserVerificationModel.query.filter_by(user_id=_id, purpose='forgotpass').order_by(UserVerificationModel.id.desc()).first()
            if verification.used == True:
                user = UserModel.find_by_id(_id)
                user.password = generate_password_hash(new_password, 'sha256')
                user.commit_to_db()

                return {'message': 'Success'}
            elif not verification.used == True:
                return {'message': 'Please check your email first!'}
            elif not verification:
                return {'message': 'Verification not found'}
            else:
                return {'message': 'Server error...'}
    
class UserVerifyForgotPassword(Resource):
    @classmethod
    def get(cls):
        _id = request.args.get('id')
        code = request.args.get('code')

        verification = UserVerificationModel.query.filter_by(user_id=_id, purpose='forgotpass').order_by(UserVerificationModel.id.desc()).first()
        if verification.used == False:
            if check_password_hash(verification.code, code) == True:
                difference_time = datetime.datetime.now() -  verification.created_at
                if difference_time.total_seconds() <= 21600:
                    verification.used = True
                    db.session.commit()
                    return {'message': 'Pass'}
                else:
                    return {'message': 'Code expired'}
            else:
                return {'message': 'Wrong verification code'}
        elif not verification.used == False:
            return {'message': 'Verification code already used!'}
        elif not verification:
            return {'message': 'Verification code not found!'}

        