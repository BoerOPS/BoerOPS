from app import db
from . import Base, TimestampMixin

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model, Base, TimestampMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    gitlab_id = db.Column(db.Integer)
    gitlab_username = db.Column(db.String(16))
    gitlab_name = db.Column(db.String(32))
    gitlab_email = db.Column(db.String(64))
    gitlab_avatar = db.Column(db.String(128))
    # project_id = db.Column(db.Integer)
    # project_name = db.Column(db.String(32))
    # ref = db.Column(db.String(32))
    # commit_id = db.Column(db.String(64))
    # commit_msg = db.Column(db.Text)
    # commit_url = db.Column(db.Text)
    # commit_timestamp = db.Column(db.String(32))
    # user_id = db.Column(db.Integer)
    # user_username = db.Column(db.String(16))
    # user_name = db.Column(db.String(16))
    # user_email = db.Column(db.String(64))

    def generate_auth_token(self, expires):
        s = Serializer(
            current_app.config['SECRET_KEY'],
            expires_in=expires,
            salt=current_app.config['SALT'])
        return s.dumps({'uid': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(
            current_app.config['SECRET_KEY'],
            salt=current_app.config['SALT'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username
