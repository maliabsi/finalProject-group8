"""Models for the DB"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class Users(UserMixin, db.Model):

    """Definition of Users Class"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15))
    first = db.Column(db.String(20))
    last = db.Column(db.String(20))
    stytchid = db.Column(db.String(60))
    email = db.Column(db.String(60))
