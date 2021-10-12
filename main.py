import flask
from flask.json import jsonify
import dotenv
import flask_login
import os
from flask_sqlalchemy import SQLAlchemy
import userdata
import spotify_calls

root_endpoint = "https://api.spotify.com/v1/"

dotenv.load_dotenv(dotenv.find_dotenv())

app = flask.Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql" + os.getenv("DATABASE_URL")[8:]
)  # replace the initial 'postgres' with 'postgresql' because heroku is stupid and doesn't let you modify the config var
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

userdata.init_login_manager(app, db)


@app.route("/login")
def login():
    return flask.render_template("/login.html")


@app.route("/validate_login", methods=["POST"])
def validate_login():
    username = flask.request.form["username"]
    try:
        user = userdata.login(username)
        return jsonify({"valid": user != None})
    except:
        return jsonify({"valid": False}), 500


def create_artists_list(artists):
    result = []
    token = spotify_calls.get_spotify_token()
    for artist in artists:
        tracks = spotify_calls.get_random_artist_tracks(artist.artist_id, token)
        artist_map = {
            "name": spotify_calls.get_artist_info(artist.artist_id, token)["name"],
            "tracks": tracks,
        }
        result.append(artist_map)
    return result


def create_recommended_artists_list(artists):
    result = []
    token = spotify_calls.get_spotify_token()
    for artist in artists:
        artist_info = spotify_calls.get_artist_info(artist.artist_id, token)
        recommended_artists = spotify_calls.get_related_artists(artist.artist_id, token)
        result.append(
            {"artist_name": artist_info["name"], "artists": recommended_artists}
        )
    return result


@app.route("/")
@flask_login.login_required
def index():
    artists = None
    saved_artists = None
    recommended_artists = None
    try:
        artists = userdata.get_saved_artists()
        saved_artists = create_artists_list(artists)
        recommended_artists = create_recommended_artists_list(artists)
    except Exception:
        pass

    return flask.render_template(
        "/dashboard.html",
        saved_artists=saved_artists,
        recommended_artists=recommended_artists,
    )


@app.route("/logout")
@flask_login.login_required
def logout():
    userdata.logout()
    return flask.redirect("/login")


@app.route("/signup")
def signup():
    return flask.render_template("/signup.html")


@app.route("/validate_signup", methods=["POST"])
def validate_signup():
    username = flask.request.form["username"]
    try:
        if not userdata.user_exists(username):
            userdata.User.create(username)
            userdata.login(username)

            return jsonify({"valid": True})
        else:
            return jsonify({"valid": False})
    except:
        return jsonify({}), 500


"""
@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()
"""

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host=os.getenv("IP", "0.0.0.0"), port=os.getenv("PORT", 8080))
