from app import db
from . import Base, TimestampMixin


class Test(db.Model, Base, TimestampMixin):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))