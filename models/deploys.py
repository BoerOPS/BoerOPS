from app import db
from . import Base, TimestampMixin


class Deploy(db.Model, Base, TimestampMixin):
    __tablename__ = 'deploys'

    id = db.Column(db.Integer, primary_key=True)
    # 0: deploy recode created; 1: prepare code; 2: exec before commands; 3: deploy code; 4: exec after commands
    status = db.Column(db.Integer)
    project_id = db.Column(
        db.Integer, db.ForeignKey('projects.id'), nullable=False)
    branch_id = db.Column(db.String(32))
    commit_id = db.Column(db.String(64))
    env = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    introduce = db.Column(db.Text)
    deployer = db.relationship('User', backref='deploys', lazy=True)
    project = db.relationship('Project', backref='deploys', lazy=True)
