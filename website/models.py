'''
Date: 2021-10-30 20:04:06
LastEditors: GC
LastEditTime: 2021-11-02 13:06:31
FilePath: \Flask-Project\website\models.py
'''

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # One user have many notes. Store a foreign key on the child object that reference the parental object. So every time we
    #   have a note, we can figure out which user created it by looking at the user_id
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


# Set up the user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    notes = db.relationship("Note")
