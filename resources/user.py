from flask import request
from flask_restful import Resource, reqparse, Api
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from db import db
from mail import mail
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

        try:
            if data['password']:
                password_to_input = generate_password_hash(data['password'], 'sha256')
        except Exception as e:
            return {"message": e}, 200

        data_to_input = UserModel(
            username=data['username'],
            password=password_to_input,
            email=data['email'],
            ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        )

        data_to_input.save_to_db()

        randint = randint(100000, 999999)
        code = generate_password_hash(randint, 'sha256')
        data_to_input_verification = UserVerificationModel(
            user_id = UserModel.find_by_username(data['username']).with_entities(UserModel.id),
            code = code,
            purpose = 'register',
            ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        )

        return {
            "message": "Success!",
            "username": data['username'],
            "verification_code": randint,
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
                'message': 'Success',
                'user_id': user.id,
                'username': data['username'],
                'email': user.email,
                'token': token
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

class UserInitialSetup(Resource):
    @jwt_required
    def post(cls):
        data = request.get_json(force=True)
        user = UserModel.find_by_id(data['id'])

        if user['id']:
            if user['activated'] == True:
                d, m, y = data['dob'].split('-') # dd-mm-yyyy
                user.dob = datetime.datetime(int(y), int(m), int(d))

                try:
                    if data['gender'] == 'male':
                        user.gender = 'male'
                    elif data['gender'] == 'female':
                        user.gender = 'female'
                except Exception as e:
                    return {"message": e}, 200
                    
                try:
                    if data['lang'] == 'eng':
                        user.lang = user_lang.ENG
                    elif data['lang'] == 'idn':
                        user.lang = user_lang.IDN
                except Exception as e:
                    return {"message": e}, 200
                
                data_to_input_health = UserHealthHistoryModel(
                    height = data['height'],
                    weight = data['weight'],
                    activity_level = data['activity_level'],
                    sport_difficulty = data['sport_difficulty'],
                    vegan = data['vegan'],
                    maintain_weight = data['maintain_weight']
                )
                
                allergy_dict = []
                data_to_input_allergy = UserAllergyHistoryModel(
                    user_id = user.id,
                    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                )
                for item in allergy_dict:
                    data_to_input.allergy.append(AllergyModel.find_by_id(item))
                
                disease_dict = []
                data_to_input_disease = UserDiseaseHistoryModel(
                    user_id = user.id,
                    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                )
                for item in disease_dict:
                    data_to_input_disease.append(DiseaseModel.find_by_id(item))

                addiction_dict = []
                data_to_input_addiction = UserAddictionHistoryModel(
                    user_id = user.id,
                    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                )
                for item in addiction_dict:
                    data_to_input_addiction.append(AddictionModel.find_by_id(item))

                user.commit_to_db()
                data_to_input_health.save_to_db()
                data_to_input_allergy.save_to_db()
                data_to_input_disease.save_to_db()
                data_to_input_addiction.save_to_db()

            elif user['activated'] == False:
                return jsonify({
                    'message': 'Please activate first!'
                })
        elif not user['id']:
            return jsonify({
                'message': 'No user id found!'
            })
        else:
            return jsonify({
                'message': 'Server error'
            })

class UserActivation(Resource):
    @classmethod
    def post(cls):
        # ?id=....&code=.....
        _id = request.args.get('id')
        code = request.args.get('code')

        verification = UserVerificationModel.find_by_user_id(_id)
        if verification:
            if check_password_hash(verification.code, code) == True:
                user = UserModel.find_by_id(_id)
                user.activated = 1
                user.commit_to_db()

                return jsonify({
                    'message': 'Success! Now you may login.'
                })
            elif check_password_hash(verification.code, code) == False:
                return jsonify({
                    'message': 'Wrong verification code!'
                })
        elif not verification:
            return jsonify({
                'message': 'No user id found'
            })
        else:
            return jsonify({
                'message': 'Server error..'
            })

class UserForgotPasswordInit(Resource):
    @classmethod
    def post(cls):
        data = request.get_json(force=True) #{ 'identity': 'aurelius@vito' or 'auvito' }
        user = UserModel.find_by_email(data['identity']) or UserModel.find_by_username(data['identity'])
        if user:
            randint = randint(100000, 999999)
            code = generate_password_hash(randint, 'sha256')
            data_to_input_verification = UserVerificationModel(
                user_id = UserModel.find_by_username(data['username']).with_entities(UserModel.id),
                code = code,
                purpose = 'forgotpass',
                ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            )
            data_to_input_verification.save_to_db()

            msg = Message('Sirkadian Lupa Password', sender = 'sirkadiancorporation@gmail.com', recipients = [user.email])
            msg.html = "<h3>Lupa Password Sirkadian</h3><br><p>Klik link <a href='sirkadian.com/forgot_password?id=" + user.id + "&code=" + randint + "'>ini untuk mengatur ulang password Anda.</a><br><p>Abaikan pesan ini jika tidak merasa lupa password</p><br></p>Terima kasih</p><br><p>Regards, Sirkadian</p>"
            mail.send(msg)

            return jsonify({
                'message': 'Success! Silahkan cek email Anda'
            })
        else:
            return jsonify({
                'message': 'User tidak ditemukan'
            })

class UserForgotPasswordVerify(Resource):
    @classmethod
    def get(cls):
        _id = request.args.get('id')
        code = request.args.get('code')

        verification = UserVerificationModel.find_by_user_id(_id)

        if user_forgot:
            if check_password_hash(verification.code, code) == True:
                difference_time = datetime.now() -  verification.created_at
                if difference_time.total_seconds() <= 21600:
                    session['messages'] = 'pass'
                    return redirect(flask.url_for('change_password_process'), session['messages'], session['user_id'])
                else:
                    session['messages'] = 'Code expired'
                    return redirect(flask.url_for('change_password'), session['messages'])
            else:
                session['messages'] = 'Wrong verification code!'
                return redirect(flask.url_for('change_password'), session['messages'])
        elif not user_forgot:
            session['messages'] = 'Verification code not found!'
            return redirect(flask.url_for('change_password'), session['messages'])

class UserChangePassword(Resource):
    @classmethod
    def post(cls):
        new_password = request.form['new_password']
        new_password_confirm = request.form['new_password_confirm']

        _id = session[['user_id']]
        user = UserModel.find_by_id(_id)
        user.password = generate_password_hash(data['new_password'], 'sha256')
        user.commit_to_db()

        return redirect(flask.url_for('change_password'), messages={'message': 'Success'})