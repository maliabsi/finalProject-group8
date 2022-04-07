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
    stytchid = db.Column(db.String(60))
    email = db.Column(db.String(60))


class Communties(db.Model, Base):
    """Communities table created"""

    id = db.Column(db.Integer, primary_key=True)
    community_name = db.Column(db.String(120), nullable=False)
    creator_user_id = relationship("Users", foreignkeys="Users.id")
    num_of_collaborators = db.Column(db.Integer, nullable=False)
    num_of_events = db.Column(db.Integer, nullable=False)
    num_of_charties = db.Column(db.Integer, nullable=False)


class Events(db.Model, Base):
    """Events table created"""

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(120), nullable=False)
    creator_user_id = relationship("Users", foreignkeys="Users.id")
    num_of_collaborators = db.Column(db.Integer, nullable=False)
    event_decription = db.Column(db.String(500), nullable=False)
    event_date = db.Column(db.String(120), nullable=False)
    event_time = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    num_of_event_participants = db.Column(db.String(120), nullable=False)
    community_id = relationship("Communities", foreignkeys="Communities.id")


class Participants(db.Model, Base):
    """Participants table created"""

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(120), nullable=False)
    participant_user_id = relationship("Users", foreignkeys="Users.id")
    event_id = db.Column(db.Integer, nullable=False, ForeignKey=True)


class Colaborators(db.Model, Base):
    """Colaborators table created"""

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(120), nullable=False)
    collaborator_user_id = relationship("Users", foreignkeys="Users.id")
    event_id = relationship("Events", foreignkeys="Events.id")
