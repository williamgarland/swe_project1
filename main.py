import flask
from flask.json import jsonify
import flask_login
import dotenv
import os
from flask_login.utils import logout_user
from flask_sqlalchemy import SQLAlchemy

dotenv.load_dotenv(dotenv.find_dotenv())

app = flask.Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

# Point SQLAlchemy to your Heroku database
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@localhost/songoracle"  # os.getenv('DATABASE_URL')
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

users = {}


class User(flask_login.UserMixin):
    def __init__(self, uid):
        self.id = uid

    def get(uid):
        # from models import DBUser

        # user = DBUser.query().filter_by(username=uid).first()
        # if user is None:
        #    return user
        # return User(user.username)
        # return User(uid=uid)
        if uid in users:
            return users[uid]
        return None

    def create(uid):
        if uid in users:
            return None
        result = User(uid=uid)
        users[uid] = result
        return result


@login_manager.user_loader
def load_user(uid):
    return User.get(uid)


@app.route("/login")
def login():
    return flask.render_template("/login.html")


@app.route("/validate_login", methods=["POST"])
def validate_login():
    username = flask.request.form["username"]
    user = User.get(username)
    if user:
        flask_login.login_user(user, remember=True)
    return jsonify({"valid": user != None})


@app.route("/")
@flask_login.login_required
def index():
    return flask.render_template("/dashboard.html")


@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect("/login")


@app.route("/signup")
def signup():
    return flask.render_template("/signup.html")


@app.route("/validate_signup", methods=["POST"])
def validate_signup():
    username = flask.request.form["username"]
    user = User.get(username)
    print("user: " + str(user))
    if user == None:
        # Add the user to the database and log in
        # TODO: Add the user to the database
        user = User.create(username)
        flask_login.login_user(user, remember=True)

        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False})


app.run(debug=True)
