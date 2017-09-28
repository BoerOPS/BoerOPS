from app import db
from . import Base

class Test(Base, db.Model):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    create_at = db.Column(db.DateTime, default=db.func.now())
    update_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
