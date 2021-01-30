from flask import request
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
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

#class InitialLoad:
# ambil user id dari request
# UserModel find by id get username, email, profile img, cover img urls
# user health history select limit 1 by user id get tb, bb
# user sleep history select limit 5 by user id get name, kkal
# user food history select limit 5 by user id get name, kkal
# user meditation history select limit 5 by user id get name, duration
# user sport history select limit 5 by user id get names, duration
# user mood histoory select limit 1 by user id get mood, date created
# user points select limit 1 by user id get user points
# var user_level = user_points / 1000 bulatkan 1 digit
# return setelah format jadi 1 json

# class Briefing:
# get user_id, pagi/siang/malam
# from food import necessity_calculator

# class TodayStatus:
# get user_id
# var current_food_kkal, current_sport_kkal, last_sleep duration, last mood
# get kkal from user_food_history where date.now sampai date.now 00:00
# get kkal from user_sport_history where date.now sampai date.now 00:00
# user_sleep_history limit 1 get duration
# user_mood_history limit 1 get mood

# class ProfilePage:
# get user_id
# user_food_history get date, name, kkal limit 5 by date.now - 7days by user id
# user_sport_history get date, name, kkal limit 5 by date.now - 7days by user id
# user_meditation_history get date, duration limit 5 by date.now - 7days by user id
# user_song_history get date, song limit 5 by date.now - 7 days by user id
# user_adiksi_history get date, adiksi limit 5 by date.now - 7days by user id
# return json