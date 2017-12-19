from app import db
from . import Base, TimestampMixin


class Host(db.Model, Base, TimestampMixin):
    __tablename__ = 'hosts'

    id = db.Column(db.Integer, primary_key=True)
    ip_addr = db.Column(db.String(16))
    env = db.Column(db.Integer)