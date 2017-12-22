from app import db
from . import Base, TimestampMixin

rel_project_host = db.Table('rel_project_host',
                            db.Column(
                                'project_id',
                                db.Integer,
                                db.ForeignKey('projects.id'),
                                primary_key=True),
                            db.Column(
                                'host_id',
                                db.Integer,
                                db.ForeignKey('hosts.id'),
                                primary_key=True),
                            db.Column(
                                'created_at',
                                db.DateTime,
                                default=db.func.now()),
                            db.Column(
                                'updated_at',
                                db.DateTime,
                                default=db.func.now(),
                                onupdate=db.func.now()))


class Project(db.Model, Base, TimestampMixin):
    __tablename__ = 'projects'

    # id = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    before_checkout = db.Column(db.Text)
    after_checkout = db.Column(db.Text)
    before_deploy = db.Column(db.Text)
    after_deploy = db.Column(db.Text)

    hosts = db.relationship(
        'Host',
        secondary=rel_project_host,
        backref=db.backref('projects', lazy='dynamic'))
