"""Runs the app and sets up DB if initial run. """
import os
import json
import flask

from dotenv import find_dotenv, load_dotenv
from flask_login import current_user, LoginManager, login_user, logout_user
from stytch import Client
from models import db, Users, Communties, Events, Participants, Colaborators
from stytch_tools import stytch_auth, get_user_data


load_dotenv(find_dotenv())
app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("NEW_DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
login_manager = LoginManager()
login_manager.init_app(app)


# Database stuff
db.init_app(app)
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    """loads  current user"""
    return Users.query.get(int(user_id))


@app.route("/")
def index():
    """index page: more!"""
    return flask.render_template("index.html")


import os
import flask

from dotenv import find_dotenv, load_dotenv
from flask_login import current_user, LoginManager, login_user, logout_user
from stytch import Client
from models import db, Users


load_dotenv(find_dotenv())
app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("NEW_DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    """loads  current user"""
    return Users.query.get(int(user_id))


@app.route("/")
def index():
    """index page: more!"""
    return flask.render_template("index.html")


# This needs to be tested live. Stytch will not send to a  non-https:// URL.
@app.route("/sign-up")
def signup():
    """signup methond"""
    return flask.render_template("sign-up.html")


@app.route("/authenticate")
def authenticate():
    """Authenticator for logging in/signing up. Redirected here from OAuth with a token URL param"""

    # Retrieve token from url params
    token = flask.request.args.get("token")

    # Temporary mock for token until test is written.
    # token = "SeiGwdj5lKkrEVgcEY3QNJXt6srxS3IK2Nwkar6mXD4="

    # Authenticates
    response = client.oauth.authenticate(token)

    # If the response is a 200, the user is verified and can be logged in
    # (Copied from Stytch API docs)
    if response.status_code == 200:
        if Users.query.filter_by(token=token).first is None:
            flask.redirect(flask.url_for("signup"), token)
    # Authenticates and retrieves stytch user_id from response
    stytch_id = stytch_auth(token)
    # stytch_id = "user-test-552d704c-39b0-4c02-a0a1-f9d71a7473d9"

    # If stytch_auth does not ruturn null value
    if stytch_id:

        visitor = Users.query.filter_by(stytch_id=stytch_id).first()

        # Logs in user if they exist already
        if visitor:
            login_user(visitor)
            print(get_user_data(visitor.stytch_id))
            return flask.redirect(flask.url_for("index"))

        # Otherwise adds them to db, then logs them in
        visitor = Users(stytch_id=stytch_id)
        db.session.add(visitor)
        db.session.commit()
        login_user(visitor)
        return flask.redirect(flask.url_for("index"))

    print("Not authorized")
    flask.flash("We were unable to authenticate you. Please try again.")
    return flask.redirect(flask.url_for("index"))


@app.route("/stytch_login")
def stytch_login():
    """Temporary stytch login page"""
    return flask.render_template(
        "login_stytch.html",
        GOOGLE_OAUTH_URL=os.getenv("GOOGLE_OAUTH_URL"),
        FBOOK_OAUTH_URL=os.getenv("FBOOK_OATH_URL"),
    )


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/communities")
def visit_communities():
    return flask.render_template("communities.html")


@app.route("/sign-up")
def signup():
    return flask.render_template("sign-up.html")


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/communities")
def visit_communities():
    return flask.render_template("communities.html")


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
