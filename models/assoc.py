from db import db

food_user_assoc = db.Table('food_user_assoc', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

food_history_assoc = db.Table('food_history_assoc', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('history_id', db.Integer, db.ForeignKey('user_food_history.id')),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

food_ingredients_assoc = db.Table('food_ingredients_assoc', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
    db.Column('ingredients_id', db.Integer, db.ForeignKey('food_ingredients.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

food_ingredients_info_assoc = db.Table('food_ingredients_info_assoc', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
    db.Column('info', db.Integer, db.ForeignKey('food_ingredients_info.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

food_instructions_assoc = db.Table('food_instructions_assoc', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
    db.Column('instructions', db.Integer, db.ForeignKey('food_instructions.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

trending_food_assoc = db.Table('trending_food_assoc', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
    db.Column('analytics_id', db.Integer, db.ForeignKey('analytics_food.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

sport_history_assoc = db.Table('sport_history_assoc', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('history_id', db.Integer, db.ForeignKey('user_sport_history.id')),
    db.Column('sport_id', db.Integer, db.ForeignKey('sport.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

disease_history_assoc = db.Table('disease_history_assoc', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('history_id', db.Integer, db.ForeignKey('user_disease_history.id')),
    db.Column('disease_id', db.Integer, db.ForeignKey('disease.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

addiction_history_assoc = db.Table('addiction_history_assoc', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('history_id', db.Integer, db.ForeignKey('user_addiction_history.id')),
    db.Column('addiction_id', db.Integer, db.ForeignKey('addiction.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

allergy_history_assoc = db.Table('allergy_history_assoc', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('history_id', db.Integer, db.ForeignKey('user_allergy_history.id')),
    db.Column('allergy_id', db.Integer, db.ForeignKey('allergy.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

meditation_history_assoc = db.Table('meditation_history_assoc', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('history_id', db.Integer, db.ForeignKey('user_meditation_history.id')),
    db.Column('meditation_id', db.Integer, db.ForeignKey('meditation.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

song_history_assoc = db.Table('song_history_assoc', db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('history_id', db.Integer, db.ForeignKey('user_song_history.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

# tag_food_assoc = db.Table('tag_food_assoc', db.Model.metadata,
#     db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
#     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
#     db.Column('created_at', db.DateTime, default=db.func.now())
# )