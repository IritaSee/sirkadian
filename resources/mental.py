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
from models.mental import (
    MeditationModel,
    SongModel
)
from models.assoc import (
    food_ingredients_assoc
)
from datetime import (
    date
)
import datetime
# class AddMoodHistory:

# class QuoteEngine:

class AddMeditation(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('mental/add_meditation.html'),200,headers)
    def post(self):
        req = request.form.to_dict()
        meditation_name = req['meditation_name']
        meditation_mood = req['meditation_mood']
        meditation_duration = req['meditation_duration']

        # First of all, check apakah makanan ini udh ada
        if MeditationModel.find_by_name(meditation_name):
            return {"message": "Meditation already exists"}, 400

        # file processing
        if 'meditation_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['meditation_file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], "meditation_file", filename))

        
        db.session.add(MeditationModel(
            name=meditation_name,
            mood=meditation_mood,
            duration=meditation_duration,
            filename=filename
            ))

        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error tambah meditasi!')
            return redirect(request.url)

        flash('Sukses tambah meditasi!')
        return redirect(request.url)

# class AddMeditationHistory:

# class MeditationTrending:

# class MeditationDetail:

class AddSong(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('mental/add_song.html'),200,headers)
    def post(self):
        req = request.form.to_dict()
        song_name = req['song_name']
        song_artist = req['song_artist']
        song_mood = req['song_mood']
        song_duration = req['song_duration']

        # First of all, check apakah makanan ini udh ada
        if SongModel.find_by_name(song_name):
            return {"message": "Meditation already exists"}, 400

        # file processing
        if 'song_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['song_file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], "song_file", filename))

        
        db.session.add(SongModel(
            name=song_name,
            artist=song_artist,
            mood=song_mood,
            duration=song_duration,
            filename=filename
            ))

        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error tambah lagu!')
            return redirect(request.url)

        flash('Sukses tambah lagu!')
        return redirect(request.url)

# class AddSongHistory:

# class SongTrending:

# class SongDetail:

# class AddAddictionHistory:

# class GetAddictionHistory: