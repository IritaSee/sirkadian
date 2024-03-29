from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
from sqlalchemy import event
import flask_admin as admin

from db import db
from mail import mail
from blacklist import *
from config import *

from resources.user import *
from resources.food import *
from resources.tags import *
from resources.addiction import *
from resources.allergy import *
from resources.disease import *
from resources.mental import *
from resources.sleep import *
from resources.sport import *

from models.addiction import *
from models.allergy import *
from models.mental import *

import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)


app = Flask(__name__)
if app.config["ENV"] == "production":
    app.config.from_object("config.DevelopmentConfig")
else:
    app.config.from_object("config.ProductionConfig")

ma = Marshmallow(app)

db.init_app(app)

migrate = Migrate(app, db)

mail.init_app(app)


from models import *


manager = Manager(app)
manager.add_command('db', MigrateCommand)

api = Api(app)
jwt = JWTManager(app)


# token related
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decoded_token):
    return is_token_revoked(decoded_token)

@jwt.expired_token_loader
def expired_token_callback():
    return {
      'description': 'The token has expired',
      'error': 'token_expired'
    }, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        'message': 'Signature verification failed'
    }, 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return {
        'message': 'Request does not contain an access token'
    }, 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return {
        'message': 'The token is not fresh'
    }, 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return {
        'message': 'The token has been revoked',
    }, 401

# from flask_sqlalchemy import get_debug_queries
# app.config['SQLALCHEMY_RECORD_QUERIES'] = True
# @app.after_request
# def after_request_func(response):
#     for query in get_debug_queries():
#         if query.duration >= 0:
#             print(query.statement, query.parameters, query.duration, query.context)
#     return response


    # if request.method == 'POST':
    #     if response.status_code == 405:
    #         print(response.json['message'])
    #         request_data = {"url": request.environ["REQUEST_URI"], "ip": request.remote_addr}
    #         FORMAT = '%(asctime)s %(message)s %(url)s %(ip)s'
    #         logging.basicConfig(filename='demo.log', format=FORMAT, datefmt='%d/%m/%Y %I:%M:%S %p')
    #         logging.warning("POST", extra=request_data)
    #         return response
    # return response

# resource related to general website
@app.route('/')
def indexgeneral():
    return render_template('home.html')

# route related to admining
@app.route('/admin_only')
def indexadmin():
    return render_template('baseadmin.html')

# related to user
@app.route('/forgot_password', methods = ['GET'], endpoint='change_password')
def change_password():
    return render_template('user/change_password.html')

@event.listens_for(FoodModel, 'after_delete')
def del_image(mapper, connection, target):
    if target.image_filename:
        list_files = cdn.list_files({"name": target.image_filename})
        try : 
            fileId = list_files['response'][0]['fileId']
            cdn.delete_file(fileId)
        except Exception as e:
            pass

api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/user/register')
api.add_resource(UserInitialSetup, '/user/initial') # post
api.add_resource(UserActivation, '/user/activate') # post
api.add_resource(UserForgotPassword, '/user/forgot/<int:option>') # alur: post option 1, get, post option 2
api.add_resource(UserVerifyForgotPassword, '/user/forgot/verify')
api.add_resource(UserLogin, '/user/login')
api.add_resource(UserLogout, '/user/logout')
api.add_resource(TokenRefresh, '/user/refresh')

# resource related to food
api.add_resource(AddFood, '/api/food/add_food_interface')
api.add_resource(GetAllFoodAPI, '/api/food/get_all_food_api')
api.add_resource(GetAllFoodIngredientsAPI, '/api/food/get_all_food_ingredients_api')
api.add_resource(GetFoodById, '/api/food/get/<int:food_id>')
api.add_resource(GetIngredientsById, '/api/food/ingredients/get/<int:ingredient_id>')
api.add_resource(FoodTrending, '/api/food/trending')
api.add_resource(FoodDetail, '/api/food/detail')
api.add_resource(FoodNutrition, '/api/food/nutrition')
api.add_resource(FoodRecipe, '/api/food/recipe')
api.add_resource(FoodHistory, '/api/food/history')
api.add_resource(FoodNecessity, '/api/food/necessity')
api.add_resource(FoodRecommendation, '/api/food/recommendation')
api.add_resource(FoodRating, '/api/food/rating')
# belum finish: necessity

# resource related to addiction
api.add_resource(AddAddiction, '/api/addiction/add_addiction_interface')

# resource related to allergy
api.add_resource(AddAllergy, '/api/allergy/add_allergy')
api.add_resource(SearchAllergy, '/api/allergy/get_allergy')

# resource related to disease
api.add_resource(AddDisease, '/api/disease/add_disease_interface')

# resource related to mental
api.add_resource(AddMeditation, '/api/meditation/add_meditation_interface')
api.add_resource(AddSong, '/api/song/add_song_interface')

# resource related to sport
api.add_resource(AddSport, '/api/sport/add_sport_interface')
api.add_resource(Sport, '/sport/<int:sport_id>')

# resource related to tagging
api.add_resource(AddTag, '/admin_only/add_tag')
api.add_resource(GetAllTagsAPI, '/admin_only/get_tags')

from admin import (
    AllergyModelAdmin,
    FoodModelAdmin,
    FoodIngredientsModelAdmin
)
admin = admin.Admin(app, template_mode='bootstrap3')
admin.add_view(AllergyModelAdmin())
admin.add_view(FoodModelAdmin())
admin.add_view(FoodIngredientsModelAdmin())

if __name__ == '__main__':
    manager.run()
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)