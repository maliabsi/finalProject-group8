"""Models for the DB"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db = SQLAlchemy()


class Users(UserMixin, db.Model, Base):
    """Users table created"""

    id = db.Column(db.Integer, primary_key=True)
    stytch_id = db.Column(db.String(60))
    email = db.Column(db.String(60))
    created_communities = relationship("Communities")
    communities = db.Column(db.ARRAY(db.Integer))


class Communities(db.Model, Base):
    """Communities table created"""

    id = db.Column(db.Integer, primary_key=True)
    community_name = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(120))
    description = db.Column(db.String(600), nullable=False)
    creator_user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    members = db.Column(db.ARRAY(db.Integer))
    events = relationship("Events")


class Events(db.Model, Base):
    """Events table created"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    creator_user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    tagline = db.Column(db.String(120))
    decription = db.Column(db.String(600), nullable=False)
    date = db.Column(db.String(120), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey(Communities.id))
    participants = db.Column(db.ARRAY(db.Integer))
