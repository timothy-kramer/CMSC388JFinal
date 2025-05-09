from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager, utils
from mongoengine import StringField, ImageField, ReferenceField, IntField
#from wtforms.validators import (
#    InputRequired,
#    Length,
#    Email,
#    EqualTo,
#    ValidationError,
#)


# TODO: implement
@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

# TODO: implement fields
class User(db.Document, UserMixin):
    username = StringField(required=True, unique=True, min_length=1, max_length=40)
    email = StringField(required=True, unique=True)
    password = StringField(required=True) 
    profile_pic = db.ImageField()

    # Returns unique string identifying our object
    def get_id(self):
        # TODO: implement
        return str(self.username)


# TODO: implement fields
class Review(db.Document):
    commenter = ReferenceField(User, required=True)  
    content = StringField(required=True, min_length=5, max_length=500)
    date = StringField(required=True) 
    imdb_id = StringField(required=True, min_length=9, max_length=9)  
    movie_title = StringField(required=True, min_length=1, max_length=100)
    image = db.ImageField()
    #Uncomment when other fields are ready for review pictures

#watchlist class
class Watchlist(db.Document):
    user = ReferenceField(User, required=True)
    imdb_id = StringField(required=True, min_length=9, max_length=9)
    movie_title = StringField(required=True, min_length=1, max_length=100)
    priority = IntField(required=True, min_value=1, max_value=10)  # Priority from 1 to 10
    date_added = StringField(required=True, default=utils.current_time())