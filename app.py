"""Runs the app and sets up DB if initial run. """
import os
import flask

from dotenv import find_dotenv, load_dotenv
from flask_login import (
    current_user,
    LoginManager,
    login_required,
    login_user,
    logout_user,
)
from models import db, Users, Communities, Events

# from models import db, Users, Communties, Events, Participants, Colaborators
from stytch_tools import stytch_auth, get_user_data

load_dotenv(find_dotenv())
app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("NEW_DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize db and create all tables if not already.
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


@app.route("/authenticate")
def authenticate():
    """Authenticator for logging in/signing up. Redirected here from OAuth with a token URL param"""

    # Retrieve token from url params
    token = flask.request.args.get("token")

    # Temporary mock for token until test is written.
    # token = "SeiGwdj5lKkrEVgcEY3QNJXt6srxS3IK2Nwkar6mXD4="

    # Authenticates and retrieves stytch user_id from response
    stytch_id = stytch_auth(token)
    # stytch_id = "user-test-552d704c-39b0-4c02-a0a1-f9d71a7473d9"

    # If stytch_auth does not ruturn null value
    if stytch_id:
        visitor = Users.query.filter_by(stytch_id=stytch_id).first()

        # Logs in user if they exist already
        if visitor:
            login_user(visitor)
            return flask.redirect(flask.url_for("index"))

        # Otherwise adds them to db, then logs them in
        visitor = Users(stytch_id=stytch_id)
        db.session.add(visitor)
        db.session.commit()
        login_user(visitor)
        return flask.redirect(flask.url_for("index"))

    flask.flash("We were unable to authenticate you. Please try again.")
    return flask.redirect(flask.url_for("index"))


@app.route("/login")
def login():
    """OAuth login"""
    return flask.render_template(
        "login.html",
        GOOGLE_OAUTH_URL=os.getenv("GOOGLE_OAUTH_URL"),
        FBOOK_OAUTH_URL=os.getenv("FBOOK_OATH_URL"),
    )


@app.route("/communities")
def visit_communities():
    all_communties = Communities.query.all()
    community_ids = all_communties
    return flask.render_template("communities.html")


@app.route("/community")
def vist_singular_community():
    if flask.request.method == "POST":
        data = flask.request.form
        requested_community_id = Communities.query.filter_by(
            id=data["Community_id"]
        ).first()
        all_communties = Communities.query.all()
        print(db.session.query(Communities).all())
    return flask.render_template("communities.html")


@app.route("/new_community_handler")
@login_required
def add_community_handler():
    if flask.request.method == "POST":
        data = flask.request.form
        new_community = Communities(
            community_name=data["community_name"],
            tagline=data["tagline"],
            decription=data["decription"],
            creator_user_id=current_user.id,
            members=[],
            events=[],
        )
        db.session.add(new_community)
        db.session.commit()
    return flask.redirect("/community")


@app.route("/new_event_handler")
@login_required
def add_event_handler():

    if flask.request.method == "POST":
        data = flask.request.form
        new_event = Events(
            name=data["event_name"],
            creator_user_id=current_user.id,
            tagline=data["tagline"],
            decription=data["decription"],
            date=data["date"],
            time=["time"],
            community_id=data["community_id"],
            participants=[],
        )
        db.session.add(new_event)
        db.session.commit()
    return flask.redirect("/event")


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
