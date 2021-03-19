import json
import os
from sqlalchemy.orm import load_only
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
    UserHealthHistoryModel,
    UserAllergyHistoryModel
)
from models.food import (
    FoodModel,
    FoodIngredientsModel,
    FoodRecipeIngredientsModel,
    FoodAnalyticsModel,
    FoodIngredientsInfoModel,
    FoodInstructionsModel,
    FoodHelperModel,
    FoodRatingModel
)
from models.assoc import (
    food_ingredients_assoc,
    allergy_history_assoc,
    allergy_ingredients_assoc,
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
from models.allergy import AllergyModel
from datetime import (
    date
)
import datetime
from sqlalchemy import and_
from cdn import cdn

class AddFood(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return redirect('/admin/foodmodel/')
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
        image = request.files['food_image']

        if image.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if image:
            filename = secure_filename(food_name)
            upload = cdn.upload_file(
                file= image, # required
                file_name= filename, # required
                options= {
                    "folder" : "/food_image/",
                    "is_private_file": False,
                    "use_unique_file_name": True,
                    "response_fields": ["file_name"],
                }
            )
            filename = upload['response']['name']

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

        data_to_input = FoodHelperModel(
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

        # Input for trigger only then Delete
        db.session.add(data_to_input)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error tambah makanan!')
            return redirect(request.url)
        db.session.add(data_to_input)

        row_update = FoodModel.query.order_by(FoodModel.id.desc()).first()

        for item in ingredient_dict:
            ingredient_to_db = FoodIngredientsModel.find_by_id(item)
            row_update.food_ingredients.append(ingredient_to_db)

        for item in ingredient_all:
            row_update.food_ingredients_info.append(FoodIngredientsInfoModel(ingredients_info = item))
            db.session.add(FoodIngredientsInfoModel(ingredients_info = item))

        for item in instructions:
            row_update.food_instructions.append(FoodInstructionsModel(instructions = item))
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
    def get(self):
        # send json user id
        # ?option=...&id=...&type=...&page=...
        # 1=initial recommendation, 2=by number of food
        # type 1=pokok, type 2=lauk, type 3=sayur
        _id = request.args.get('id')
        option = request.args.get('option')
        page = request.args.get('page', 1, int)
        food_type = request.args.get('type')

        list_nutrisi=['vit_a','vit_b1','vit_c']

        necessity = UserNecessityModel.query.filter_by(user_id=_id).first()

        # User allergy name
        subquery1 = db.session.query(allergy_history_assoc.c.allergy_id).join(UserAllergyHistoryModel).filter(and_(UserAllergyHistoryModel.id == allergy_history_assoc.c.history_id, UserAllergyHistoryModel.user_id == _id)).subquery()

        # Allergen ingredients
        subquery2 = db.session.query(allergy_ingredients_assoc.c.ingredients_id).filter(allergy_ingredients_assoc.c.allergy_id.in_(subquery1)).subquery()

        # Foods that contain allergen ingredients
        subquery3 = db.session.query(food_ingredients_assoc.c.food_id).filter(food_ingredients_assoc.c.ingredients_id.in_(subquery2)).subquery()

        # Foods that do not exceed daily intake limit
        food = FoodModel.query.filter(FoodModel.id.notin_(subquery3)).filter(and_(
                FoodModel.calorie/FoodModel.serving <= necessity.calorie,
                FoodModel.protein/FoodModel.serving <= necessity.protein,
                FoodModel.fat/FoodModel.serving <= necessity.fat,
                FoodModel.carbohydrate/FoodModel.serving <= necessity.carbohydrate,
                FoodModel.fiber/FoodModel.serving <= necessity.fiber,
                FoodModel.calcium/FoodModel.serving <= necessity.calcium,
                FoodModel.phosphor/FoodModel.serving <= necessity.phosphor,
                FoodModel.iron/FoodModel.serving <= necessity.iron,
                FoodModel.sodium/FoodModel.serving <= necessity.sodium,
                FoodModel.potassium/FoodModel.serving <= necessity.potassium,
                FoodModel.copper/FoodModel.serving <= necessity.copper,
                FoodModel.zinc/FoodModel.serving <= necessity.zinc,
                FoodModel.vit_a/FoodModel.serving <= necessity.vit_a,
                FoodModel.vit_b1/FoodModel.serving <= necessity.vit_b1,
                FoodModel.vit_b2/FoodModel.serving <= necessity.vit_b2,
                FoodModel.vit_b3/FoodModel.serving <= necessity.vit_b3,
                FoodModel.vit_c/FoodModel.serving <= necessity.vit_c))

        if option == '1':
            pokok = FoodModel.query.filter_by(name='Nasi Putih').first()
            best_lauk = food.filter(FoodModel.food_type.like('lauk')).order_by(FoodModel.nutri_point.desc()).limit(20).all()
            best_sayur = food.filter(FoodModel.food_type.like('sayur')).order_by(FoodModel.nutri_point.desc()).limit(20).all()

            kecocokan_lauk = {}
            kecocokan_sayur = {}

            for idx, number in enumerate(best_lauk):
                kecocokan_lauk[best_lauk[idx].id] = {}
                for value in list_nutrisi:
                    try:
                        kecocokan_lauk[best_lauk[idx].id][value] = getattr(best_lauk[idx],value)/getattr(necessity,value)
                    except:
                        kecocokan_lauk[best_lauk[idx].id][value] = getattr(best_lauk[idx],value)
            for idx, number in enumerate(best_sayur):
                kecocokan_sayur[best_sayur[idx].id] = {}
                for value in list_nutrisi:
                    try:
                        kecocokan_sayur[best_sayur[idx].id][value] = getattr(best_sayur[idx],value)/getattr(necessity,value)
                    except:
                        kecocokan_sayur[best_sayur[idx].id][value] = getattr(best_sayur[idx],value)

            total_kecocokan_lauk = {}
            total_kecocokan_sayur = {}

            for key, data in kecocokan_lauk.items():
                total_kecocokan_lauk[key] = sum(data.values())
            for key, data in kecocokan_sayur.items():
                total_kecocokan_sayur[key] = sum(data.values())

            bobot_rating_lauk = max(total_kecocokan_lauk.values()) - min(total_kecocokan_lauk.values()) / 2.5
            bobot_rating_sayur = max(total_kecocokan_sayur.values()) - min(total_kecocokan_sayur.values()) / 2.5

            result_lauk = []
            result_sayur = []

            rekomendasi_bersama_lauk = []
            rekomendasi_bersama_sayur = []


            #
            # GANTI number.protein -> number.rating
            #

            for identity, data in total_kecocokan_lauk.items():
                for idx, number in enumerate(best_lauk):
                    if best_lauk[idx].id == identity:
                        rekomendasi = data + (bobot_rating_lauk * number.protein)
                        rekomendasi_bersama_lauk.append(rekomendasi)
                        result_lauk.append({'id': identity, 'name': number.name, 'rekomendasi': rekomendasi, 'image_filename': number.image_filename})
            for identity, data in total_kecocokan_sayur.items():
                for idx, number in enumerate(best_sayur):
                    if best_sayur[idx].id == identity:
                        rekomendasi = data + (bobot_rating_sayur * number.protein)
                        rekomendasi_bersama_sayur.append(rekomendasi)
                        result_sayur.append({'id': identity, 'name': number.name, 'rekomendasi': rekomendasi, 'image_filename': number.image_filename})
                        

            max_rekomendasi_lauk = max(rekomendasi_bersama_lauk)
            max_rekomendasi_sayur = max(rekomendasi_bersama_sayur)


            for data in result_lauk:
                for key, value in data.items():
                    if key == 'rekomendasi':
                        data[key] = data[key]/max_rekomendasi_lauk*10
            for data in result_sayur:
                for key, value in data.items():
                    if key == 'rekomendasi':
                        data[key] = data[key]/max_rekomendasi_sayur*10

            return jsonify({'lauk':result_lauk},{'sayur':result_sayur})

        elif option == '2':
            max_per_page = 2
            if food_type == '1': # pokok
                pokok = FoodModel.query.filter_by(name='Nasi Putih').first()
            elif food_type == '2': # lauk
                best_lauk = food.filter(FoodModel.food_type.like('lauk')).order_by(FoodModel.nutri_point.desc()).paginate(page=page, error_out=True, max_per_page=max_per_page)
        
                kecocokan_lauk = {}
                
                for idx, number in enumerate(best_lauk.items):
                    kecocokan_lauk[best_lauk.items[idx].id] = {}
                for value in list_nutrisi:
                    try:
                        kecocokan_lauk[best_lauk.items[idx].id][value] = getattr(best_lauk.items[idx],value)/getattr(necessity,value)
                    except:
                        kecocokan_lauk[best_lauk.items[idx].id][value] = getattr(best_lauk.items[idx],value)

                total_kecocokan_lauk = {}

                for key, data in kecocokan_lauk.items():
                    total_kecocokan_lauk[key] = sum(data.values())

                bobot_rating_lauk = max(total_kecocokan_lauk.values()) - min(total_kecocokan_lauk.values()) / 2.5

                result_lauk = []

                rekomendasi_bersama_lauk = []

                #
                # GANTI number.protein -> number.rating
                #

                for identity, data in total_kecocokan_lauk.items():
                    for idx, number in enumerate(best_lauk.items):
                        if best_lauk.items[idx].id == identity:
                            rekomendasi = data + (bobot_rating_lauk * number.protein)
                            rekomendasi_bersama_lauk.append(rekomendasi)
                            result_lauk.append({'id': identity, 'name': number.name, 'rekomendasi': rekomendasi, 'image_filename': number.image_filename})

                max_rekomendasi_lauk = max(rekomendasi_bersama_lauk)
                for data in result_lauk:
                    for key, value in data.items():
                        if key == 'rekomendasi':
                            data[key] = data[key]/max_rekomendasi_lauk*10
                            return jsonify({'lauk':result_lauk})

            elif food_type == '3': # sayur
                best_sayur = food.filter(FoodModel.food_type.like('sayur')).order_by(FoodModel.nutri_point.desc()).paginate(page=page, error_out=True, max_per_page=max_per_page)

                kecocokan_sayur = {}
                
                for idx, number in enumerate(best_sayur.items):
                    kecocokan_sayur[best_sayur.items[idx].id] = {}
                    for value in list_nutrisi:
                        try:
                            kecocokan_sayur[best_sayur.items[idx].id][value] = getattr(best_sayur.items[idx],value)/getattr(necessity,value)
                        except:
                            kecocokan_sayur[best_sayur.items[idx].id][value] = getattr(best_sayur.items[idx],value)
        
                total_kecocokan_sayur = {}

                for key, data in kecocokan_sayur.items():
                    total_kecocokan_sayur[key] = sum(data.values())

                bobot_rating_sayur = max(total_kecocokan_sayur.values()) - min(total_kecocokan_sayur.values()) / 2.5

                result_sayur = []

                rekomendasi_bersama_sayur = []

                #
                # GANTI number.protein -> number.rating
                #

                for identity, data in total_kecocokan_sayur.items():
                    for idx, number in enumerate(best_sayur.items):
                        if best_sayur.items[idx].id == identity:
                            rekomendasi = data + (bobot_rating_sayur * number.protein)
                            rekomendasi_bersama_sayur.append(rekomendasi)
                            result_sayur.append({'id': identity, 'name': number.name, 'rekomendasi': rekomendasi, 'image_filename': number.image_filename})
                              
                max_rekomendasi_sayur = max(rekomendasi_bersama_sayur)

                for data in result_sayur:
                    for key, value in data.items():
                        if key == 'rekomendasi':
                            data[key] = data[key]/max_rekomendasi_sayur*10

                return jsonify({'sayur':result_sayur})
            else:
                return jsonify({'message': 'Please enter food type!'})
        else:
            return jsonify({'message': 'Please enter option!'})

    def post(self):
        # send foods that have eaten, deduct value from necessity table
        pass

class FoodRating(Resource):
    @classmethod
    def post(self): #?id=...&food=...&rating=...
        user_id = request.args.get('id')
        food_id = int(request.args.get('food'))
        rating = int(request.args.get('rating'))
        ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

        existing_rating = FoodRatingModel.query.filter(and_(FoodRatingModel.user_id == user_id,FoodRatingModel.food_id == food_id)).first()

        if rating == 0:
            return jsonify({'message': "Don't put zero"})

        if existing_rating is not None:
            #hitung rating
            food_rating = FoodRatingModel.query.filter_by(food_id=food_id).all()

            food_to_change = FoodModel.query.filter_by(id=food_id).options(load_only('rating')).first()
            print(existing_rating)
            count_rating = 0

            rating_food = 0
            for item in food_rating:
                if item.id != user_id:
                    rating_food = rating + item.rating
                    count_rating += 1

            rating_food = rating_food / count_rating
            rating_food = round(rating, 1)
            
            #input db
            existing_rating.rating = rating
            food_to_change.rating = rating_food
            
            try:
                db.session.commit()
                return jsonify({'message': 'Success'})
            except:
                return jsonify({'message': 'Error database 4'})

            return None

        elif existing_rating is None:
            #hitung rating
            food = FoodRatingModel.query.filter_by(food_id=food_id).all()

            food_to_change = FoodModel.query.filter_by(id=food_id).options(load_only('rating')).first()
            
            rating_food = rating
            count_rating_food = 1

            for item in food:
                rating_food = rating_food + item.rating
                count_rating_food += 1
            
            rating_food = rating_food / count_rating_food
            rating_food = round(rating_food, 1)

            food_to_change.rating = rating_food

            db.session.add(FoodRatingModel(
                user_id = user_id,
                food_id = food_id,
                rating = rating,
                ip_address = ip_address
            ))

            try:
                db.session.commit()
                return jsonify({'message': 'Success'})
            except:
                return jsonify({'message': 'Error database 5'})
        else:
            return jsonify({'message': 'Error database 6'})
    
    @classmethod
    def get(self): #?food=...
        food_id = request.args.get('food')

        try:
            food = FoodRatingModel.query(func.avg(FoodRatingModel.rating)).filter_by(food_id=food_id)
        except:
            return jsonify({'message': 'Error database'})
        
        # rating = 0
        # count_rating = 0
        # for item in food:
        #     rating = rating + food.rating
        #     count_rating + 1
    
        # rating = rating / count_rating
        # rating = round(rating, 1)

        return jsonify({'food_id': food_id, 'rating': food})


class FoodNecessity(Resource):
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
        target_calorie = 0
        target_protein = 0
        target_fat = 0
        target_carbohydrate = 0
        target_fiber = 0
        target_calcium = 0
        target_phosphor = 0
        target_iron = 0
        target_sodium = 0
        target_potassium = 0
        target_copper = 0
        target_zinc = 0
        target_vit_a = 0
        target_vit_b1 = 0
        target_vit_b2 = 0
        target_vit_b3 = 0
        target_vit_c = 0
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

        if user_maintain_weight == 0: # mempertahankan
            target_calorie = target_calorie 
        elif user_maintain_weight == 1: # diet ringan
            target_calorie = target_calorie - 250
        elif user_maintain_weight == 2: # diet medium
            target_calorie = target_calorie - 500
        elif user_maintain_weight == 3: # diet keras
            target_calorie = target_calorie - 750
        elif user_maintain_weight == 4: # tambah bb ringan
            target_calorie = target_calorie + 250
        elif user_maintain_weight == 5: # tambah bb medium
            target_calorie = target_calorie + 500
        elif user_maintain_weight == 6: # tambah bb banyak bet
            target_calorie = target_calorie + 750

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

        exists_data = UserNecessityModel.query.filter_by(user_id=user_data.id).first()

        if not exists_data :
            db.session.add(UserNecessityModel(
                user_id = user_data.id,
                calorie = round(target_calorie, 1),
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
        else:
            exists_data.calorie = round(target_calorie, 1),
            exists_data.protein = round(target_protein, 1),
            exists_data.fat = round(target_fat, 1),
            exists_data.carbohydrate = round(target_carbohydrate, 1),
            exists_data.fiber = round(target_fiber, 1),
            exists_data.calcium = round(target_calcium, 1),
            exists_data.phosphor = round(target_phosphor, 1),
            exists_data.iron = round(target_iron, 1),
            exists_data.sodium = round(target_sodium, 1),
            exists_data.potassium = round(target_potassium, 1),
            exists_data.copper = round(target_copper, 1),
            exists_data.zinc = round(target_zinc, 1),
            exists_data.vit_a = round(target_vit_a, 1),
            exists_data.vit_b1 = round(target_vit_b1, 1),
            exists_data.vit_b2 = round(target_vit_b2, 1),
            exists_data.vit_b3 = round(target_vit_b3, 1),
            exists_data.vit_c = round(target_vit_c, 1),
            exists_data.ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            db.session.commit()
        except:
            return {'message': 'Error database!'}

        return jsonify({
            'user_id': user_data.id,
            'user_gender': user_gender,
            'user_age': user_age,
            'bmi': float(round(bmi, 1)),
            'calorie': round(target_calorie, 1),
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
