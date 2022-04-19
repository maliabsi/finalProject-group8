# pylint: disable=no-member
# pylint: disable=too-few-public-methods

"""Models for the DB"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db = SQLAlchemy()


class Users(UserMixin, db.Model, Base):
    """Attributes of User"""

    id = db.Column(db.Integer, primary_key=True)
    stytch_id = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60))
    created_communities = relationship("Community")
    followed_communities = relationship("Follow")
    attending_events = relationship("Attending")


class Community(db.Model, Base):
    """Attributes of Community"""

    id = db.Column(db.Integer, primary_key=True)
    community_name = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(600), nullable=False)
    creator_user_id = db.Column(db.Integer, ForeignKey(Users.id), nullable=False)
    donation_link = db.Column(db.String(120))
    members = relationship("Follow")
    events = relationship("Event")


class Event(db.Model, Base):
    """Attributes of Event"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    creator_user_id = db.Column(db.Integer, ForeignKey(Users.id), nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    decription = db.Column(db.String(600), nullable=False)
    date = db.Column(db.String(120), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    community_id = db.Column(db.Integer, ForeignKey(Community.id))
    participants = relationship("Attending")


class Follower(db.Model, Base):
    """Attributes of Follower"""

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, ForeignKey(Users.id))
    community_id = db.Column(db.Integer, ForeignKey(Community.id))


class Attendee(db.Model, Base):
    """Attributes of Attendee"""

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, ForeignKey(Users.id))
    event_id = db.Column(db.Integer, ForeignKey(Event.id))
