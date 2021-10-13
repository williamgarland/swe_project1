import flask
from flask.json import jsonify
import dotenv
import os
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
import userdata
import spotify_calls

root_endpoint = "https://api.spotify.com/v1/"

dotenv.load_dotenv(dotenv.find_dotenv())

app = flask.Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Point SQLAlchemy to your Heroku database
"""
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql" + os.getenv("DATABASE_URL")[8:]
)  # replace the initial 'postgres' with 'postgresql' because heroku is stupid and doesn't let you modify the config var
"""
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("LOCAL_DATABASE_URL")
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
    except Exception as e:
        print(str(e))
        return jsonify({"valid": False}), 500


def create_artists_list(artists, limit=5):
    result = []
    token = spotify_calls.get_spotify_token()
    as_list = list(artists)
    limit = min(limit, len(artists))
    for i in range(0, limit):
        artist = as_list[i]
        tracks = spotify_calls.get_random_artist_tracks(artist, token, limit=3)
        artist_map = {
            "name": spotify_calls.get_artist_info(artist, token)["name"],
            "tracks": tracks,
        }
        result.append(artist_map)
    return result


def create_recommended_artists_list(artists, limit=5):
    result = []
    token = spotify_calls.get_spotify_token()
    as_list = list(artists)
    limit = min(limit, len(artists))
    for i in range(0, limit):
        artist = as_list[i]
        artist_info = spotify_calls.get_artist_info(artist, token)
        recommended_artists = spotify_calls.get_related_artists(artist, token, limit=3)
        result.append({"name": artist_info["name"], "artists": recommended_artists})
    return result


@app.route("/")
@login_required
def index():
    artists = None
    saved_artists = None
    recommended_artists = None
    try:
        artists = userdata.get_saved_artists()
    except:
        pass

    try:
        saved_artists = create_artists_list(artists)
    except:
        pass

    try:
        recommended_artists = create_recommended_artists_list(artists)
    except:
        pass

    return flask.render_template(
        "/dashboard.html",
        saved_artists=saved_artists,
        recommended_artists=recommended_artists,
    )


@app.route("/logout")
@login_required
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


@app.route("/search")
@login_required
def search():
    artists = None
    try:
        search_input = flask.request.args.get("search_input")
        matches = spotify_calls.search_for_artist(search_input)
        artists = []
        for match in matches:
            artists.append(
                {
                    "artist_id": match["artist_id"],
                    "name": match["name"],
                    "top_song_id": match["top_song_id"],
                    "top_song_name": match["top_song_name"],
                    "image_url": match["image_url"],
                    "saved_by_user": userdata.has_saved_artist(match["artist_id"]),
                }
            )
    except Exception:
        pass
    return flask.render_template("search.html", artists=artists)


@app.route("/save-artist", methods=["POST"])
@login_required
def save_artist():
    try:
        artist_id = flask.request.form["artist_id"]
        userdata.add_saved_artist(artist_id)
        return jsonify({"success": True})
    except Exception:
        return jsonify({"success": False})


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.close()


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host=os.getenv("IP", "0.0.0.0"), port=os.getenv("PORT", 8080))
