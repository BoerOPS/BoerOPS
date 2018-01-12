from app import db
from . import Base, TimestampMixin


class DeployLog(db.Model, Base, TimestampMixin):
    __tablename__ = 'deploylogs'

    id = db.Column(db.Integer, primary_key=True)
    log = db.Column(db.String(256))
    readed = db.Column(db.Integer)
    deploy_id = db.Column(
        db.Integer, db.ForeignKey('deploys.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', backref='logs', lazy=True)
    deploy = db.relationship('Deploy', backref='log', lazy=True)
