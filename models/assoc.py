from db import db

# define assoc table
food_user_assoc = db.Table('food_user_assoc', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

food_ingredients_assoc = db.Table('food_ingredients_assoc', db.Model.metadata,
    db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
    db.Column('ingredients_id', db.Integer, db.ForeignKey('food_ingredients.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

trending_food_assoc = db.Table('trending_food_assoc', db.Model.metadata,
    db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
    db.Column('analytics_id', db.Integer, db.ForeignKey('analytics_food.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

sport_assoc = db.Table('sport_assoc', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user_sport_history.id')),
    db.Column('sport_id', db.Integer, db.ForeignKey('sport.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

disease_assoc = db.Table('disease_assoc', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user_disease_history.id')),
    db.Column('disease_id', db.Integer, db.ForeignKey('disease.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

addiction_assoc = db.Table('addiction_assoc', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user_addiction_history.id')),
    db.Column('addiction_id', db.Integer, db.ForeignKey('addiction.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

allergy_assoc = db.Table('allergy_assoc', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user_allergy_history.id')),
    db.Column('allergy_id', db.Integer, db.ForeignKey('allergy.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

meditation_assoc = db.Table('meditation_assoc', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user_meditation_history.id')),
    db.Column('meditation_id', db.Integer, db.ForeignKey('meditation.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

song_assoc = db.Table('song_assoc', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user_song_history.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('created_at', db.DateTime, default=db.func.now())
)

# tag_food_assoc = db.Table('tag_food_assoc', db.Model.metadata,
#     db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
#     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
#     db.Column('created_at', db.DateTime, default=db.func.now())
# )