import flask
from flask.json import jsonify
import flask_login
import dotenv
import os
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

# from sqlalchemy.orm.scoping import scoped_session
# from sqlalchemy.orm.session import sessionmaker

dotenv.load_dotenv(dotenv.find_dotenv())

app = flask.Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql" + os.getenv("DATABASE_URL")[8:]
)  # replace the initial 'postgres' with 'postgresql' because heroku is stupid and doesn't let you modify the config var
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Session = scoped_session(sessionmaker(bind=db.engine))


class User(flask_login.UserMixin):
    def __init__(self, uid):
        self.id = uid

    def get(uid):
        from models import DBUser

        user = DBUser.query.filter_by(username=uid).first()
        if user is None:
            return user
        return User(user.username)

    def create(uid):
        # session = Session()
        result = User(uid=uid)
        db.session.add(result)
        db.session.commit()
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


"""
@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()
"""

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host=os.getenv("IP", "0.0.0.0"), port=os.getenv("PORT", 8080))
