from app import db
from . import Base

from flask_login import UserMixin

class User(Base, db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    gitlab_id = db.Column(db.Integer)
    gitlab_username = db.Column(db.String(16))
    gitlab_name = db.Column(db.String(32))
    gitlab_email = db.Column(db.String(64))
    gitlab_avatar = db.Column(db.String(128))
    # project_id = db.Column(db.Integer)
    # project_name = db.Column(db.String(32))
    # ref = db.Column(db.String(32))
    # commit_id = db.Column(db.String(64))
    # commit_msg = db.Column(db.Text)
    # commit_url = db.Column(db.Text)
    # commit_timestamp = db.Column(db.String(32))
    # user_id = db.Column(db.Integer)
    # user_username = db.Column(db.String(16))
    # user_name = db.Column(db.String(16))
    # user_email = db.Column(db.String(64))
    create_at = db.Column(db.DateTime, default=db.func.now())
    update_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
