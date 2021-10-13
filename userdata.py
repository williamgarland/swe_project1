"""
USERDATA: Contains functions and data related to login/logout functionality.
"""

from __future__ import annotations
import flask_login
import sqlalchemy.orm as orm

__login_manager = flask_login.LoginManager()
__current_user = None
int__db = None
int__Session = None


def get_login_manager():
    return __login_manager


def init_login_manager(app, db):
    global __login_manager
    global int__db
    global int__Session
    __login_manager.init_app(app)
    __login_manager.login_view = "/login"
    int__db = db
    int__Session = orm.sessionmaker(int__db.engine)


def get_db_user(uid: str):
    from models import DBUser

    session = int__Session()
    user = None
    try:
        user = session.query(DBUser).filter_by(username=uid).first()
    except:
        session.rollback()
        raise
    finally:
        session.close()
    return user


class User(flask_login.UserMixin):
    def __init__(self, uid):
        self.id = uid

    def get(uid: str) -> User:
        """
        Returns a User instance of the user with the specified ID.

        If the user does not exist, this function will return None.
        If the program could not connect to the user database, this function will throw an exception.
        """
        user = get_db_user(uid)

        # user = DBUser.query.filter_by(username=uid).first()
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
        from models import DBUser

        result = User(uid=uid)

        session = int__Session()
        try:
            id = session.query(DBUser).count()
            session.add(DBUser(id=id, username=uid))
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return result


def get_current_user() -> User:
    """
    Returns the current user, or None if no user is currently logged in.
    """
    return __current_user


@__login_manager.user_loader
def load_user(uid):
    global __current_user
    from models import DBUser

    # __current_user = DBUser.query.filter_by(username=uid).first()
    __current_user = get_db_user(uid)
    return User.get(uid)


def int__get_db_user(username: str):
    from models import DBUser

    # return DBUser.query.filter_by(username=username).first()
    return get_db_user(username)


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
        __current_user = int__get_db_user(username)
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
    global int__db
    from models import DBArtist

    user = get_current_user()

    session = int__Session()
    try:
        session.delete(
            session.query(DBArtist)
            .filter_by(artist_id=artist_id, user_id=user.id)
            .first()
        )
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    # int__db.session.delete(
    #    DBArtist.query.filter_by(artist_id=artist_id, user_id=user.id).first()
    # )
    # int__db.session.commit()


def add_saved_artist(artist_id: str, artist_name: str):
    """
    Adds the artist with the specified ID to the current user's list of saved artists.

    If no user is currently logged in or the user is not in the "artists" database, this function will throw an exception.
    If the specified artist is already in the user's list of saved artists, this function does nothing.
    """
    global int__db
    user = get_current_user()
    from models import DBArtist

    session = int__Session()
    try:
        session.add(
            DBArtist(user_id=user.id, artist_id=artist_id, artist_name=artist_name)
        )
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    # int__db.session.add(DBArtist(user_id=user.id, artist_id=artist_id))
    # int__db.session.commit()


def get_saved_artists() -> list[dict[str, str]]:
    """
    Returns a list of artist database objects associated with the current user.

    If the current user has no saved artists, this will return an empty list.
    If no user is currently logged in or the user is not in the "artists" database, this function will throw an exception.
    """
    user = get_current_user()
    if user == None:
        raise Exception("No user is currently logged in")

    artist_db = list()

    from models import DBArtist

    # artists = DBArtist.query.filter_by(user_id=user.id).all()
    artists = []
    session = int__Session()
    try:
        artists = session.query(DBArtist).filter_by(user_id=user.id).all()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    for artist in artists:
        artist_db.append(
            {"artist_id": artist.artist_id, "artist_name": artist.artist_name}
        )
    return artist_db


def has_saved_artist(artist_id: str) -> bool:
    """
    Returns true if the current user has a saved artist with the specified artist ID.

    If no user is currently logged in or the user is not in the "artists" database, this function will throw an exception.
    """
    artists = get_saved_artists()
    for artist in artists:
        if artist == artist_id:
            return True
    return False
