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
from models.allergy import (
    AllergyModel
)
from models.assoc import (
    food_ingredients_assoc
)
from datetime import (
    date
)
import datetime

class AddAllergy(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('allergy/add_allergy.html'),200,headers)
    def post(self):
        req = request.form.to_dict()
        allergy_name = req['allergy_name']

        # First of all, check apakah makanan ini udh ada
        if AllergyModel.find_by_name(allergy_name):
            return {"message": "Allergy already exists"}, 400
        
        db.session.add(AllergyModel(name=allergy_name))

        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error tambah alergi!')
            return redirect(request.url)

        flash('Sukses tambah alergi!')
        return redirect(request.url)