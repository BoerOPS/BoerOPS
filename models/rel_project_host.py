from app import db
from . import Base, TimestampMixin


class RelProjectHost(db.Model, Base, TimestampMixin):
    __tablename__ = 'rel_project_host'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'))

    host = db.relationship(
        "User", backref=db.backref("projects", lazy="dynamic"))
    project = db.relationship(
        "Project", backref=db.backref("hosts", lazy="dynamic"))