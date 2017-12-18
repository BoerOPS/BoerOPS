from app import db
from . import Base

class Host(Base, db.Model):
    __tablename__ = 'hosts'

    id = db.Column(db.Integer, primary_key=True)
    ip_addr = db.Column(db.String(16))
    env = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=db.func.now())
    update_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
