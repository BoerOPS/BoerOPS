from app import db
from . import Base, TimestampMixin


class Commit(db.Model, Base, TimestampMixin):
    __tablename__ = 'commits'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer)
    project_name = db.Column(db.String(32))
    ref = db.Column(db.String(32))
    commit_id = db.Column(db.String(64))
    commit_msg = db.Column(db.Text)
    commit_url = db.Column(db.Text)
    commit_timestamp = db.Column(db.String(32))
    user_id = db.Column(db.Integer)
    user_username = db.Column(db.String(16))
    user_name = db.Column(db.String(16))
    user_email = db.Column(db.String(64))