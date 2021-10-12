"""
USERDATA: Contains functions and data related to login/logout functionality.
"""

from __future__ import annotations
import flask_login

__login_manager = flask_login.LoginManager()
__current_user = None
__db = None


def get_login_manager():
    return __login_manager


def init_login_manager(app, db):
    global __login_manager
    global __db
    __login_manager.init_app(app)
    __login_manager.login_view = "/login"
    __db = db


int__TMP = {}
int__ARTISTS = {}


class int__TMPUSER:
    def __init__(self, username):
        self.username = username


def int__GETUSER(uid):
    if not uid in int__TMP:
        return None
    return int__TMP[uid]


class User(flask_login.UserMixin):
    def __init__(self, uid):
        self.id = uid

    def get(uid: str) -> User:
        """
        Returns a User instance of the user with the specified ID.

        If the user does not exist, this function will return None.
        If the program could not connect to the user database, this function will throw an exception.
        """
        # from models import DBUser

        # user = DBUser.query.filter_by(username=uid).first()
        user = int__GETUSER(uid)
        if user is None:
            return user
        return User(user.username)

    def create(uid: str) -> User:
        """
        Creates a user with the specified ID and returns it.

        This function does not check for duplicate users,
        so make sure you know that the specified ID is not already present in the database before calling this function.
        If the program could not connect to the user database, this function will throw an exception.
        """
        # from models import DBUser

        result = User(uid=uid)
        int__TMP[uid] = int__TMPUSER(uid)
        int__ARTISTS[uid] = set()
        # __db.session.add(DBUser(username=uid))
        # __db.session.commit()
        return result


def get_current_user() -> User:
    """
    Returns the current user, or None if no user is currently logged in.
    """
    return __current_user


@__login_manager.user_loader
def load_user(uid):
    return User.get(uid)


def login(username: str) -> User:
    """
    Logs in the user with the specified username and returns the user.
    If the user does not exist, this function will do nothing and return None.
    If the program failed to connect to the user database, this function will throw an exception.
    """
    global __current_user
    user = User.get(username)
    if user:
        flask_login.login_user(user, remember=True)
        __current_user = user
    return user


def logout():
    """
    Logs out the current user.
    After calling this function, get_current_user() will return None until login() is called again.
    """
    global __current_user
    flask_login.logout_user()
    __current_user = None


def user_exists(username: str) -> bool:
    """
    Returns true if the user with the specified username exists in the user database.
    If the program failed to connect to the user database, this function will throw an exception.
    """
    return User.get(username) != None


def remove_saved_artist(artist_id: str):
    """
    Removes the artist with the specified ID from the current user's list of saved artists.

    If no user is currently logged in or the user is not in the "artists" database, this function will throw an exception.
    If the specified artist is not in the user's list of saved artists, this function does nothing.
    """
    global int__ARTISTS
    int__ARTISTS[get_current_user().get_id()].remove(artist_id)


def add_saved_artist(artist_id: str):
    """
    Adds the artist with the specified ID to the current user's list of saved artists.

    If no user is currently logged in or the user is not in the "artists" database, this function will throw an exception.
    If the specified artist is already in the user's list of saved artists, this function does nothing.
    """
    global int__ARTISTS
    int__ARTISTS[get_current_user().get_id()].add(artist_id)


def get_saved_artists() -> set[str]:
    """
    Returns a set of artist IDs associated with the current user.

    If the current user has no saved artists, this will return an empty set.
    If no user is currently logged in or the user is not in the "artists" database, this function will throw an exception.
    """
    user = get_current_user()
    if user == None or not user.get_id() in int__ARTISTS:
        raise Exception()

    return int__ARTISTS[user.get_id()]
