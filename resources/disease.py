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
from models.disease import (
    DiseaseModel
)
from models.assoc import (
    food_ingredients_assoc
)
from datetime import (
    date
)
import datetime

class AddDisease(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('disease/add_disease.html'),200,headers)
    def post(self):
        req = request.form.to_dict()
        disease_name = req['disease_name']
        disease_organ_system = req['disease_organ_system']
        disease_food_prohibition = req['disease_food_prohibition']
        disease_sport_prohibition = req['disease_sport_prohibition']

        # First of all, check apakah makanan ini udh ada
        if DiseaseModel.find_by_name(disease_name):
            return {"message": "Disease already exists"}, 400
        
        db.session.add(DiseaseModel(
            name=disease_name,
            organ_system=disease_organ_system,
            food_prohibition=disease_food_prohibition,
            sport_prohibition=disease_sport_prohibition
            ))

        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error tambah penyakit!')
            return redirect(request.url)

        flash('Sukses tambah penyakit!')
        return redirect(request.url)