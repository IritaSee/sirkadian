from flask import Flask, jsonify, render_template, flash, current_app
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from db import db

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.food import *
from resources.tags import *

app = Flask(__name__)
if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

ma = Marshmallow(app)

db.init_app(app)

migrate = Migrate(app, db)

# import models
from models import *

manager = Manager(app)
manager.add_command('db', MigrateCommand)

api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()

# resource related to general website
@app.route('/')
def indexgeneral():
    return render_template('home.html')

# route related to admining
@app.route('/admin_only')
def indexadmin():
    return render_template('baseadmin.html')

@app.route('/admin_only/food/add_food', methods=['POST','GET'])
def add_food_interface():
    return render_template('food/add_food_interface.html')

# resource related to tagging
api.add_resource(AddTag, '/admin_only/add_tag')
api.add_resource(GetAllTagsAPI, '/admin_only/get_tags')

# resource related to user
api.add_resource(UserRegister, '/user/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/user/login')
api.add_resource(UserLogout, '/user/logout')
api.add_resource(TokenRefresh, '/user/refresh')

# resource related to food
api.add_resource(AddFood, '/admin_only/food/add_food_interface')
api.add_resource(GetAllFoodAPI, '/admin_only/food/get_all_food_api')
api.add_resource(GetAllFoodIngredientsAPI, '/admin_only/food/get_all_food_ingredients_api')
api.add_resource(GetFoodById, '/admin_only/food/get/<int:food_id>')

if __name__ == '__main__':
    manager.run()
    app.run(port=5000, debug=True)