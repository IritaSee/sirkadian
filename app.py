from flask import Flask, jsonify, render_template, flash, current_app
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from db import db

from resources.user import *
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

# resource related to tagging
api.add_resource(AddTag, '/admin_only/add_tag')
api.add_resource(GetAllTagsAPI, '/admin_only/get_tags')

# related to user
@app.route('/forgot_password', methods = ['GET'], endpoint='change_password')
def change_password():
    return render_template('user/change_password.html')

api.add_resource(UserRegister, '/user/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/user/login')
api.add_resource(UserLogout, '/user/logout')
api.add_resource(TokenRefresh, '/user/refresh')
api.add_resource(UserForgotPasswordInit, '/user/forgot_password_init')
api.add_resource(UserForgotPasswordVerify, '/user/forgot_password_verify')
api.add_resource(UserChangePassword, '/user/change_password_process', endpoint='change_password_process')

# resource related to food
api.add_resource(AddFood, '/api/food/add_food_interface')
api.add_resource(GetAllFoodAPI, '/api/food/get_all_food_api')
api.add_resource(GetAllFoodIngredientsAPI, '/api/food/get_all_food_ingredients_api')
api.add_resource(GetFoodById, '/api/food/get/<int:food_id>')
api.add_resource(FoodTrending, '/api/food/trending')
api.add_resource(FoodDetail, '/api/food/detail')
api.add_resource(FoodNutrition, '/api/food/nutrition')
api.add_resource(FoodRecipe, '/api/food/recipe')
api.add_resource(FoodHistory, '/api/food/history')
# belum finish: recipe, history, necessity


if __name__ == '__main__':
    manager.run()
    app.run(port=5000, debug=True)