"""Runs the app and sets up DB if initial run. """
import os
import flask

from dotenv import find_dotenv, load_dotenv
from flask_login import current_user, LoginManager, login_user, logout_user
from stytch import Client
import stytch
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


@app.route("/sign-up")
def signup():
    """signup methond"""
    return flask.render_template("sign-up.html")


@app.route("/authenticate")
def authenticate():
    """Authenticator for logging in/signing up. Redirected here from OAuth with a token URL param"""
    client = Client(
        project_id=os.getenv("PROJECT_ID"),
        secret=os.getenv("STYTCH_SECRET"),
        environment="test",
    )

    token = flask.request.args.get("token")
    print("token:", token)

    # Temporary mock for token until test is written.
    # token = "SeiGwdj5lKkrEVgcEY3QNJXt6srxS3IK2Nwkar6mXD4="

    # Authenticates
    response = client.oauth.authenticate(token)

    sess = client.sessions.authenticate(session_token=token)
    stytch_id = sess.user_id
    print("userid:", sess.user_id)

    # If the response is a 200, the user is verified and can be logged in
    # (Copied from Stytch API docs)
    if response.status_code == 200:
        # if True:
        if Users.query.filter_by(stytch_id=stytch_id).first() is None:
            # return flask.redirect(flask.url_for("signup"), token)
            return flask.redirect(flask.url_for("index"))

        visitor = Users.query.filter_by(stytch_id=stytch_id).first()
        login_user(visitor)
        # flask.flash(f"Welcome Back {current_user.username}!")
        return flask.redirect(flask.url_for("index"))

    print("Not authorized")
    flask.flash("Google was unable to authenticate you. Please try again.")
    return flask.redirect(flask.url_for("index"))


# @app.route("/handle_login")
# def handle_login():
#     """Temporary handle login function"""
#     return flask.redirect(flask.url_for("index"))


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


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
