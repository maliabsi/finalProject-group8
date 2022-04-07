"""Models for the DB"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class Users(UserMixin, db.Model):

    """Definition of Users Class"""

    id = db.Column(db.Integer, primary_key=True)
    stytchid = db.Column(db.String(60))
