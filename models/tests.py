from app import db
from . import BaseMinin

class Test(BaseMinin):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    create_at = db.Column(db.DateTime, default=db.func.now())
    update_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
