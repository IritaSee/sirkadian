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
from models.addiction import (
    AddictionModel
)
from models.assoc import (
    food_ingredients_assoc
)
from datetime import (
    date
)
import datetime

class AddAddiction(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('addiction/add_addiction.html'),200,headers)
    def post(self):
        req = request.form.to_dict()
        addiction_name = req['addiction_name']

        # First of all, check apakah makanan ini udh ada
        if AddictionModel.find_by_name(addiction_name):
            return {"message": "Addiction already exists"}, 400
        
        db.session.add(AddictionModel(name=addiction_name))

        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error tambah adiksi!')
            return redirect(request.url)

        flash('Sukses tambah adiksi!')
        return redirect(request.url)