import os
import json
from os.path import join, dirname, realpath
from decimal import Decimal
from flask import request, jsonify, flash, redirect, current_app, render_template, make_response
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from blacklist import *
from db import db
from models.user import (
    UserModel
)
from models.user_history import (
    UserFoodHistoryModel
)
from models.sport import (
    SportModel
)
from models.assoc import (
    food_ingredients_assoc
)
from datetime import (
    date
)
import datetime

class Sport(Resource):
    @classmethod
    def get(cls, sport_id):
        sport = SportModel.find_by_id(sport_id)
        if not sport:
            return {'message': 'Sport not found'}, 404
        return jsonify(sport.dict())

    @classmethod
    def delete(cls, user_id):
        sport = SportModel.find_by_id(sport_id)
        if not sport:
            return {'message': 'Sport not found'}, 404
        sport.delete_from_db()
        return {'message': 'Sport deleted'}, 200

class AddSport(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('sport/add_sport.html'),200,headers)
    def post(self):
        req = request.form.to_dict()
        sport_name = req['sport_name']
        sport_cps = req['sport_cps']
        sport_difficulty = req['sport_difficulty']
        sport_amount = req['sport_amount']
        sport_sets = req['sport_sets']
        sport_duration = req['sport_duration']

        # First of all, check apakah makanan ini udh ada
        if SportModel.find_by_name(sport_name):
            return {"message": "Meditation already exists"}, 400

        # file processing
        if 'sport_image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['sport_image']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], "sport_image", filename))


        db.session.add(SportModel(
            name = sport_name,
            cps = sport_cps,
            difficulty = sport_difficulty,
            amount = sport_amount,
            sets = sport_sets,
            duration = sport_duration,
            image_filename = filename
            ))

        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error tambah olahraga!')
            return redirect(request.url)

        flash('Sukses tambah olahraga!')
        return redirect(request.url)

# class TrendingSport:

# class SportRecommendation:

# class SportNecessity:

# class SportDetail:

# class AddSportHistory:

# class GetSportHistory:
