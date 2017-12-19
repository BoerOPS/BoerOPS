from app import db
from . import Base, TimestampMixin
from .rel_project_host import RelProjectHost


class Project(db.Model, Base, TimestampMixin):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    before_checkout = db.Column(db.Text)
    after_checkout = db.Column(db.Text)
    before_deploy = db.Column(db.Text)
    after_deploy = db.Column(db.Text)
    host_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer)

    hosts = db.relationship(
        "Host",
        secondary=RelProjectHost,
        backref=db.backref("projects", lazy="dynamic"))
