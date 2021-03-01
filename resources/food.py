import json
import os
from os.path import join, dirname, realpath
from decimal import Decimal
from flask import request, jsonify, flash, redirect, current_app, render_template, make_response
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
    decode_token
)
from werkzeug.utils import secure_filename
from blacklist import *
from db import db
from models.user import (
    UserModel,
    UserNecessityModel
)
from models.user_history import (
    UserFoodHistoryModel,
    UserHealthHistoryModel
)
from models.food import (
    FoodModel,
    FoodIngredientsModel,
    FoodRecipeIngredientsModel,
    FoodAnalyticsModel,
    FoodIngredientsInfoModel,
    FoodInstructionsModel
)
from models.assoc import (
    food_ingredients_assoc
)
from models.enum import (
    FoodType
)
from models.schemas import (
    FoodSchema,
    FoodIngredientsSchema,
    FoodAnalyticsSchema,
    UserFoodHistorySchema
)
from datetime import (
    date
)
import datetime

class AddFood(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('food/add_food_interface.html'),200,headers)
    def post(self):
        req = request.form.to_dict()
        food_name = req['food_name']
        food_type = req['food_type']
        food_serving = req['food_serving']
        food_duration = req['food_duration']
        food_difficulty = req['food_difficulty']
        tags = req['tags']

        # First of all, check apakah makanan ini udh ada
        if FoodModel.find_by_name(food_name):
            return {"message": "Food already exists"}, 400

        # image processing
        if 'food_image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['food_image']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], "food_image", filename))

        # Declare variable
        namabahan = []
        angkabahan = []
        satuanbahan = []
        instructions = []
        calorie = 0
        protein = 0
        fat = 0
        carbohydrate = 0
        fiber = 0
        calcium = 0
        phosphor = 0
        iron = 0
        sodium = 0
        potassium = 0
        copper = 0
        zinc = 0
        vit_a = 0
        vit_b1 = 0
        vit_b2 = 0
        vit_b3 = 0
        vit_c = 0

        # bahan processing (serializing, dkk)
        for item in req:
            if "[namabahan]" in item:
                namabahan.append(req[item])
            elif "[angkabahan]" in item:
                angkabahan.append(req[item])
            elif "[satuanbahan]" in item:
                satuanbahan.append(req[item])
            elif "[instruksimakanan]" in item:
                instructions.append(req[item])

        jumlahbahan = len(namabahan)
        
        listbahansorted = list(zip(namabahan, angkabahan, satuanbahan))
        listbahan_processed = list(zip(namabahan, angkabahan, satuanbahan))
        ingredient_all = []

        for idx, item in enumerate(listbahansorted):
            item = list(item)
            ingredient_all.append(' '.join(item))
            if "sdm" in item[2]:
                item[1] = float(item[1]) * 15
                item[2] = "gram"
                listbahan_processed[idx] = item
            elif "sdt" in item[2]:
                item[1] = float(item[1]) * 5
                item[2] = "gram"
                listbahan_processed[idx] = item
            elif "butir" in item[2]:
                item[1] = float(item[1]) * 50
                item[2] = "gram"
                listbahan_processed[idx] = item
            elif "siung" in item[2]:
                item[1] = float(item[1]) * 5
                item[2] = "gram"
                listbahan_processed[idx] = item
            elif "Minyak" in item[0]: # hilangkan perhitungan buat minyak
                item[1] = 0

        # todo: entah kenapa setelah for loop sm if else perubahan listnya
        # ga kesimpen di list jd kalkulasi berikutnya berantakan
        # update 19-01-2021 KELARRRR
        ingredient_dict = []
        
        for item in listbahan_processed:
            ingredient_db = FoodIngredientsModel.find_by_name(item[0])
            ingredient_dict.append(ingredient_db.id)
            calorie = calorie + ( ( float(item[1]) / 100 ) * ingredient_db.calorie )
            protein = protein + ( ( float(item[1]) / 100 ) * ingredient_db.protein )
            fat = fat + ( ( float(item[1]) / 100 ) * ingredient_db.fat )
            carbohydrate = carbohydrate + ( ( float(item[1]) / 100 ) * ingredient_db.carbohydrate )
            fiber = fiber + ( ( float(item[1]) / 100 ) * ingredient_db.fiber )
            calcium = calcium + ( ( float(item[1]) / 100 ) * ingredient_db.calcium )
            phosphor = phosphor + ( ( float(item[1]) / 100 ) * ingredient_db.phosphor )
            iron = iron + ( ( float(item[1]) / 100 ) * ingredient_db.iron )
            sodium = sodium + ( ( float(item[1]) / 100 ) * ingredient_db.sodium )
            potassium = potassium + ( ( float(item[1]) / 100 ) * ingredient_db.potassium )
            copper = copper + ( ( float(item[1]) / 100 ) * ingredient_db.copper )
            zinc = zinc + ( ( float(item[1]) / 100 ) * ingredient_db.zinc )
            vit_a = vit_a + ( ( float(item[1]) / 100 ) * ingredient_db.vit_a )
            vit_b1 = vit_b1 + ( ( float(item[1]) / 100 ) * ingredient_db.vit_b1 )
            vit_b2 = vit_b2 + ( ( float(item[1]) / 100 ) * ingredient_db.vit_b2 )
            vit_b3 = vit_b3 + ( ( float(item[1]) / 100 ) * ingredient_db.vit_b3 )
            vit_c = vit_c + ( ( float(item[1]) / 100 ) * ingredient_db.vit_c )
            
        data_to_input = FoodModel(
            name = food_name,
            food_type = food_type,
            duration = food_duration,
            serving = food_serving,
            difficulty = food_difficulty,
            calorie = calorie,
            protein = protein,
            fat = fat,
            carbohydrate = carbohydrate,
            fiber = fiber,
            calcium = calcium,
            phosphor = phosphor,
            iron = iron,
            sodium = sodium,
            potassium = potassium,
            copper = copper,
            zinc = zinc,
            vit_a = vit_a,
            vit_b1 = vit_b1,
            vit_b2 = vit_b2,
            vit_b3 = vit_b3,
            vit_c = vit_c,
            tags = tags,
            image_filename = filename
        )

        for item in ingredient_dict:
            ingredient_to_db = FoodIngredientsModel.find_by_id(item)
            data_to_input.food_ingredients.append(ingredient_to_db)

        for item in ingredient_all:
            data_to_input.food_ingredients_info.append(FoodIngredientsInfoModel(ingredients_info = item))
            db.session.add(FoodIngredientsInfoModel(ingredients_info = item))

        for item in instructions:
            data_to_input.food_instructions.append(FoodInstructionsModel(instructions = item))
            db.session.add(FoodInstructionsModel(instructions = item))

        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error tambah makanan!')
            return redirect(request.url)

        flash('Sukses tambah makanan!')
        return redirect(request.url)

class GetFoodById(Resource):
    @classmethod
    def get(cls, food_id):
        food = FoodModel.find_by_id(food_id)
        data = FoodSchema().dump(food)

        if not data:
            return {"message": "Food not found"}, 404

        return jsonify(data)

class GetIngredientsById(Resource):
    @classmethod
    def get(cls, ingredient_id):
        ingredient = FoodIngredientsModel.find_by_id(ingredient_id)

        data = FoodIngredientsSchema().dump(ingredient)

        if not data:
            return {"message": "Ingredient not found"}, 404

        return jsonify(data)

class GetAllFoodIngredientsAPI(Resource):
    @classmethod
    def get(cls):
        food_ingredients_schema = FoodIngredientsSchema(many=True)
        food = FoodIngredientsModel.query.with_entities(FoodIngredientsModel.id, FoodIngredientsModel.name).all()
        output = food_ingredients_schema.dump(food)
        return output

class GetAllFoodAPI(Resource):
    @classmethod
    def get(cls):
        # foods_schema = FoodSchema(many=True)
        # food = FoodModel.query.all()
        # output = foods_schema.dump(food)
        # return jsonify({'data': output})
        food = FoodModel.query.all()
        data = FoodSchema(many=True).dump(food)
        return jsonify(data)

class FoodTrending(Resource):
    @classmethod
    def get(cls):
        # sirkadian.com/trending_food?o=1&ys=2021&ms=01&ds=01&ye=2021&me=03&de=31
        # o=1 -> date filter, o=2 -> today's trending
        option = request.args.get('o')

        if option == '1':
            year_s_url = int(request.args.get('ys'))
            month_s_url = int(request.args.get('ms'))
            day_s_url = int(request.args.get('ds'))
            year_e_url = int(request.args.get('ye'))
            month_e_url = int(request.args.get('me'))
            day_e_url = int(request.args.get('de'))

            start_date = date(year=year_s_url, month=month_s_url, day=day_s_url)
            end_date = date(year=year_e_url, month=month_e_url, day=day_e_url)
            
            analytics_food = FoodAnalyticsModel.query.filter(FoodAnalyticsModel.created_at <= end_date).filter(FoodAnalyticsModel.created_at >= start_date)
            data = FoodAnalyticsSchema(many=True).dump(analytics_food)
            return jsonify(data)
        elif option == '2':
            analytics_food = FoodAnalyticsModel.query.filter(FoodAnalyticsModel.created_at <= datetime.datetime.now()).all()
            data = FoodAnalyticsSchema(many=True).dump(analytics_food)
            return jsonify(data)

    @classmethod
    def post(cls):
        option = request.args.get('o')
        if option == '1':
            data = request.get_json(force=True)
            if data['food_id']:
                data_to_input = FoodAnalyticsModel(
                    food_id = FoodModel.find_by_id(data['food_id']).id,
                    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                )
                data_to_input.save_to_db()

                return jsonify({'message': 'Success'})
            else:
                return jsonify({'message': 'Please enter food id'})
        else:
            return jsonify({'message': 'Enter valid option'})

class FoodRecommendation(Resource):
    @classmethod
    def get(cls):
        # send json user id
        pass

    def post(cls):
        # send foods that have eaten, deduct value from necessity table
        pass
        

class FoodNecessity(Resource):
    @jwt_refresh_token_required
    def get(self):
        # ?id=...
        # Food Nutrition necessity in one day.
        _id = request.args.get('id')

        user_data = UserModel.query.filter_by(id=_id).with_entities(UserModel.id, UserModel.gender, UserModel.dob).order_by(UserModel.id.desc()).first()
        user_health = UserHealthHistoryModel.query.filter_by(user_id=_id).with_entities(
            UserHealthHistoryModel.height,
            UserHealthHistoryModel.weight,
            UserHealthHistoryModel.activity_level,
            UserHealthHistoryModel.maintain_weight
        ).order_by(UserHealthHistoryModel.id.desc()).first()
        
        # Hitung BMI
        user_weight = user_health.weight
        user_height_cm = user_health.height
        user_height_m = user_health.height / 100

        bmi = user_weight / (user_height_m ** 2)

        # Hitung kalori
        user_gender = user_data.gender
        user_activity_level = user_health.activity_level
        user_maintain_weight = user_health.maintain_weight
        user_date = user_data.dob
        today_date = date.today()

        user_age = today_date.year - user_date.year - ((today_date.month, today_date.day) < (user_date.month, user_date.day))

        if user_gender == 'male':
            if user_activity_level == 'sedentary':
                    target_calorie = ( (10 * user_weight) + (6.25 * user_height_cm) - (5 * user_age) + 5 ) * 1.2
            elif user_activity_level == 'low':
                    target_calorie = ( (10 * user_weight) + (6.25 * user_height_cm) - (5 * user_age) + 5 ) * 1.37
            elif user_activity_level == 'medium':
                    target_calorie = ( (10 * user_weight) + (6.25 * user_height_cm) - (5 * user_age) + 5 ) * 1.55
            elif user_activity_level == 'high':
                    target_calorie = ( (10 * user_weight) + (6.25 * user_height_cm) - (5 * user_age) + 5 ) * 1.9
        elif user_gender == 'female':
            if user_activity_level == 'sedentary':
                    target_calorie = ( (10 * user_weight) + (6.25 * user_height_cm) - (5 * user_age) - 161 ) * 1.2
            elif user_activity_level == 'low':
                    target_calorie = ( (10 * user_weight) + (6.25 * user_height_cm) - (5 * user_age) - 161 ) * 1.37
            elif user_activity_level == 'medium':
                    target_calorie = ( (10 * user_weight) + (6.25 * user_height_cm) - (5 * user_age) - 161 ) * 1.55
            elif user_activity_level == 'high':
                    target_calorie = ( (10 * user_weight) + (6.25 * user_height_cm) - (5 * user_age) - 161 ) * 1.9
        
        if user_maintain_weight == 0:
            target_calorie_min = target_calorie - 0
            target_calorie_max = target_calorie + 0
        elif user_maintain_weight == 1:
            target_calorie_min = target_calorie - 250
            target_calorie_max = target_calorie
        elif user_maintain_weight == 2:
            target_calorie_min = target_calorie - 500
            target_calorie_max = target_calorie
        elif user_maintain_weight == 3:
            target_calorie_min = target_calorie - 750
            target_calorie_max = target_calorie
        elif user_maintain_weight == 4:
            target_calorie_min = target_calorie
            target_calorie_max = target_calorie + 250
        elif user_maintain_weight == 5:
            target_calorie_min = target_calorie
            target_calorie_max = target_calorie + 500
        elif user_maintain_weight == 6:
            target_calorie_min = target_calorie
            target_calorie_max = target_calorie + 750

        if user_gender == 'male':
            if user_age <= 12:
                target_protein = 50
                target_fat = 65
                target_carbohydrate = 300
                target_fiber = 28
                target_calcium = 1200
                target_phosphor = 1250
                target_iron = 8
                target_sodium = 1300
                target_potassium = 3900
                target_copper = 0.7
                target_zinc = 8
                target_vit_a = 600
                target_vit_b1 = 1.1
                target_vit_b2 = 1.3
                target_vit_b3 = 12
                target_vit_c = 50
            elif 13 <= user_age <= 15:
                target_protein = 70
                target_fat = 80
                target_carbohydrate = 350
                target_fiber = 34
                target_calcium = 1200
                target_phosphor = 1250
                target_iron = 11
                target_sodium = 1500
                target_potassium = 4800
                target_copper = 0.795
                target_zinc = 11
                target_vit_a = 600
                target_vit_b1 = 1.2
                target_vit_b2 = 1.3
                target_vit_b3 = 16
                target_vit_c = 75
            elif 16 <= user_age <= 18:
                target_protein = 75
                target_fat = 85
                target_carbohydrate = 400
                target_fiber = 37
                target_calcium = 1200
                target_phosphor = 1250
                target_iron = 11
                target_sodium = 1700
                target_potassium = 5300
                target_copper = 0.89
                target_zinc = 11
                target_vit_a = 700
                target_vit_b1 = 1.2
                target_vit_b2 = 1.3
                target_vit_b3 = 16
                target_vit_c = 90
            elif 19 <= user_age <= 29:
                target_protein = 65
                target_fat = 75
                target_carbohydrate = 430
                target_fiber = 37
                target_calcium = 1000
                target_phosphor = 700
                target_iron = 9
                target_sodium = 1500
                target_potassium = 4700
                target_copper = 0.9
                target_zinc = 11
                target_vit_a = 650
                target_vit_b1 = 1.2
                target_vit_b2 = 1.3
                target_vit_b3 = 16
                target_vit_c = 90
            elif 30 <= user_age <= 49:
                target_protein = 65
                target_fat = 70
                target_carbohydrate = 415
                target_fiber = 36
                target_calcium = 1000
                target_phosphor = 700
                target_iron = 9
                target_sodium = 1500
                target_potassium = 4700
                target_copper = 0.9
                target_zinc = 11
                target_vit_a = 650
                target_vit_b1 = 1.2
                target_vit_b2 = 1.3
                target_vit_b3 = 16
                target_vit_c = 90
            elif 50 <= user_age <= 64:
                target_protein = 65
                target_fat = 60
                target_carbohydrate = 340
                target_fiber = 30
                target_calcium = 1200
                target_phosphor = 700
                target_iron = 9
                target_sodium = 1300
                target_potassium = 4700
                target_copper = 0.9
                target_zinc = 11
                target_vit_a = 650
                target_vit_b1 = 1.2
                target_vit_b2 = 1.3
                target_vit_b3 = 16
                target_vit_c = 90
            elif user_age >= 65:
                target_protein = 64
                target_fat = 50
                target_carbohydrate = 275
                target_fiber = 25
                target_calcium = 1200
                target_phosphor = 700
                target_iron = 9
                target_sodium = 1100
                target_potassium = 4700
                target_copper = 0.9
                target_zinc = 11
                target_vit_a = 650
                target_vit_b1 = 1.2
                target_vit_b2 = 1.3
                target_vit_b3 = 16
                target_vit_c = 90
        elif user_gender == 'female':
            if user_age <= 12:
                target_protein = 50
                target_fat = 65
                target_carbohydrate = 300
                target_fiber = 28
                target_calcium = 1200
                target_phosphor = 1250
                target_iron = 8
                target_sodium = 1400
                target_potassium = 4400
                target_copper = 0.7
                target_zinc = 8
                target_vit_a = 600
                target_vit_b1 = 1.0
                target_vit_b2 = 1.0
                target_vit_b3 = 12
                target_vit_c = 50
            elif 13 <= user_age <= 15:
                target_protein = 70
                target_fat = 80
                target_carbohydrate = 350
                target_fiber = 34
                target_calcium = 1200
                target_phosphor = 1250
                target_iron = 15
                target_sodium = 1500
                target_potassium = 4800
                target_copper = 0.795
                target_zinc = 9
                target_vit_a = 600
                target_vit_b1 = 1.1
                target_vit_b2 = 1.0
                target_vit_b3 = 14
                target_vit_c = 65
            elif 16 <= user_age <= 18:
                target_protein = 75
                target_fat = 85
                target_carbohydrate = 400
                target_fiber = 37
                target_calcium = 1200
                target_phosphor = 1250
                target_iron = 15
                target_sodium = 1600
                target_potassium = 5000
                target_copper = 0.89
                target_zinc = 9
                target_vit_a = 600
                target_vit_b1 = 1.1
                target_vit_b2 = 1.0
                target_vit_b3 = 14
                target_vit_c = 75
            elif 19 <= user_age <= 29:
                target_protein = 65
                target_fat = 75
                target_carbohydrate = 430
                target_fiber = 37
                target_protein = 75
                target_fat = 85
                target_carbohydrate = 400
                target_fiber = 37
                target_calcium = 1000
                target_phosphor = 700
                target_iron = 18
                target_sodium = 1500
                target_potassium = 4700
                target_copper = 0.9
                target_zinc = 8
                target_vit_a = 600
                target_vit_b1 = 1.1
                target_vit_b2 = 1.0
                target_vit_b3 = 14
                target_vit_c = 75
            elif 30 <= user_age <= 49:
                target_protein = 65
                target_fat = 70
                target_carbohydrate = 415
                target_fiber = 36
                target_calcium = 1000
                target_phosphor = 700
                target_iron = 18
                target_sodium = 1500
                target_potassium = 4700
                target_copper = 0.9
                target_zinc = 8
                target_vit_a = 600
                target_vit_b1 = 1.1
                target_vit_b2 = 1.0
                target_vit_b3 = 14
                target_vit_c = 75
            elif 50 <= user_age <= 64:
                target_protein = 65
                target_fat = 60
                target_carbohydrate = 340
                target_fiber = 30
                target_calcium = 1200
                target_phosphor = 700
                target_iron = 8
                target_sodium = 1400
                target_potassium = 4700
                target_copper = 0.9
                target_zinc = 8
                target_vit_a = 600
                target_vit_b1 = 1.1
                target_vit_b2 = 1.0
                target_vit_b3 = 14
                target_vit_c = 75
            elif user_age >= 65:
                target_protein = 64
                target_fat = 50
                target_carbohydrate = 275
                target_fiber = 25
                target_calcium = 1200
                target_phosphor = 700
                target_iron = 8
                target_sodium = 1200
                target_potassium = 4700
                target_copper = 0.9
                target_zinc = 8
                target_vit_a = 600
                target_vit_b1 = 1.1
                target_vit_b2 = 1.0
                target_vit_b3 = 14
                target_vit_c = 75

        db.session.add(UserNecessityModel(
            user_id = user_data.id,
            calorie_min = round(target_calorie_min, 1),
            calorie_max = round(target_calorie_max, 1),
            protein = round(target_protein, 1),
            fat = round(target_fat, 1),
            carbohydrate = round(target_carbohydrate, 1),
            fiber = round(target_fiber, 1),
            calcium = round(target_calcium, 1),
            phosphor = round(target_phosphor, 1),
            iron = round(target_iron, 1),
            sodium = round(target_sodium, 1),
            potassium = round(target_potassium, 1),
            copper = round(target_copper, 1),
            zinc = round(target_zinc, 1),
            vit_a = round(target_vit_a, 1),
            vit_b1 = round(target_vit_b1, 1),
            vit_b2 = round(target_vit_b2, 1),
            vit_b3 = round(target_vit_b3, 1),
            vit_c = round(target_vit_c, 1),
            ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        ))

        try:
            db.session.commit()
        except:
            return {'message', 'Error database!'}

        return jsonify({
            'user_id': user_data.id,
            'user_gender': user_gender,
            'user_age': user_age,
            'bmi': float(round(bmi, 1)),
            'calorie_min': round(target_calorie_min, 1),
            'calorie_max': round(target_calorie_max, 1),
            'protein': round(target_protein, 1),
            'fat': round(target_fat, 1),
            'carbohydrate': round(target_carbohydrate, 1),
            'fiber': round(target_fiber, 1),
            'calcium': round(target_calcium, 1),
            'phosphor': round(target_phosphor, 1),
            'iron': round(target_iron, 1),
            'sodium': round(target_sodium, 1),
            'potassium': round(target_potassium, 1),
            'copper': round(target_copper, 1),
            'zinc': round(target_zinc, 1),
            'vit_a': round(target_vit_a, 1),
            'vit_b1': round(target_vit_b1, 1),
            'vit_b2': round(target_vit_b2, 1),
            'vit_b3': round(target_vit_b3, 1),
            'vit_c': round(target_vit_c, 1)
        })

class FoodDetail(Resource):
    @classmethod
    def get(cls):
        # sirkadian.com/admin_only/food/food_detail?o=1&id=28
        # o=1 -> all detail, o=2 -> half detail
        option = request.args.get('o')

        if option == '1':
            _id = request.args.get('id')
            food_detail = FoodModel.find_by_id(_id)
            data = FoodSchema().dump(food_detail)
            return jsonify(data)
        elif option == '2':
            _id = request.args.get('id')
            food_half_detail = FoodModel.query.filter_by(id=_id).with_entities(FoodModel.name, FoodModel.duration, FoodModel.calorie, FoodModel.food_type).first()
            data = FoodSchema().dump(food_half_detail)
            return jsonify(data)

class FoodNutrition(Resource):
    @classmethod
    def get(cls):
        _id = request.args.get('id')

        food_nutrition = FoodModel.query.filter_by(id=_id).with_entities(
            FoodModel.calorie,
            FoodModel.protein,
            FoodModel.fat,
            FoodModel.carbohydrate,
            FoodModel.fiber,
            FoodModel.calcium,
            FoodModel.phosphor,
            FoodModel.iron,
            FoodModel.sodium,
            FoodModel.potassium,
            FoodModel.copper,
            FoodModel.zinc,
            FoodModel.vit_a,
            FoodModel.vit_b1,
            FoodModel.vit_b2,
            FoodModel.vit_b3,
            FoodModel.vit_c
        ).first()

        data = FoodSchema().dump(food_nutrition)
        return jsonify(data)

class FoodRecipe(Resource):
    @classmethod
    def get(cls):
        _id = request.args.get('id')
        food = FoodModel.query.filter_by(id=_id).first()
        data = FoodSchema(exclude=[
            'calorie',
            'protein',
            'fat',
            'carbohydrate',
            'fiber',
            'calcium',
            'phosphor',
            'iron',
            'sodium',
            'potassium',
            'copper',
            'zinc',
            'vit_a',
            'vit_b1',
            'vit_b2',
            'vit_b3',
            'vit_c',
            'tags'
            ]).dump(food)

        # food_ingredients_info_str = 
        # print(food_ingredients_info_str)
        # data['food_ingredients_info'] = json.loads(food_ingredients_info_str)

        return jsonify(data)

class FoodHistory(Resource):
    @classmethod
    def get(cls):
        # sirkadian.com/food_history?o=1&ys=2021&ms=01&ds=01&ye=2021&me=03&de=31
        # o=1 -> date filter, o=2 -> today's history,
            # o=3 _> ft == 1=breakfast 2=lunch 3= dinner 4=snack
        option = request.args.get('o')

        if option == '1':
            year_s_url = int(request.args.get('ys'))
            month_s_url = int(request.args.get('ms'))
            day_s_url = int(request.args.get('ds'))
            year_e_url = int(request.args.get('ye'))
            month_e_url = int(request.args.get('me'))
            day_e_url = int(request.args.get('de'))

            start_date = date(year=year_s_url, month=month_s_url, day=day_s_url)
            end_date = date(year=year_e_url, month=month_e_url, day=day_e_url)
            
            history_food = UserFoodHistoryModel.query.filter(UserFoodHistoryModel.created_at <= end_date).filter(UserFoodHistoryModel.created_at >= start_date)
            data = UserFoodHistorySchema(many=True).dump(history_food)
            return jsonify(data)
        elif option == '2':
            history_food = UserFoodHistoryModel.query.filter(UserFoodHistoryModel.created_at <= date.today())
            data = UserFoodHistorySchema(many=True).dump(history_food)
            return jsonify(data)
        elif option == '3':
            food_type_url = request.args.get('ft')
            if food_type_url == 1:
                history = UserFoodHistoryModel.query.filter_by(food_type='breakfast').all()
                data = UserFoodHistorySchema(many=True).dump(history)
                return jsonify(data)
            elif food_type_url == 2:
                history = UserFoodHistoryModel.query.filter_by(food_type='lunch').all()
                data = UserFoodHistorySchema(many=True).dump(history)
                return jsonify(data)
            elif food_type_url == 3:
                history = UserFoodHistoryModel.query.filter_by(food_type='dinner').all()
                data = UserFoodHistorySchema(many=True).dump(history)
                return jsonify(data)
            elif food_type_url == 4:
                history = UserFoodHistoryModel.query.filter_by(food_type='snack').all()
                data = UserFoodHistorySchema(many=True).dump(history)
                return jsonify(data)

    @classmethod
    def post(cls):
        data = request.get_json(force=True)

        user_id = data['user_id']
        food_ids = data['food_id']
        food_type = data['food_type']
        ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

        find_user = UserModel.query.filter_by(id=user_id).first()
        data_to_input = UserFoodHistoryModel(
            user_id = find_user.id,
            food_type = data['food_type'],
            ip_address = ip_address
        )

        total_calorie = 0
        for item in food_ids:
            find_food = FoodModel.find_by_id(item['id'])
            total_calorie = total_calorie + find_food.calorie

            data_to_input.food.append(find_food)
        
        data_to_input.total_calorie = total_calorie
        data_to_input.save_to_db()
        
        return jsonify({
            'message': 'Success!'
        })