from main import db
from datetime import datetime

USER_STATUS_INACTIVE = 0
USER_STATUS_ACTIVE = 1

# ID username status creation_date last_login_date last_logout_date
class DBUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=USER_STATUS_ACTIVE)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login_date = db.Column(db.DateTime, nullable=True)
    last_logout_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "<User %r>" % self.username


# ID users(ID) artist_id
class DBArtist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("db_user.id"))
    artist_id = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Artist {self.user_id}, {self.artist_id}>"
