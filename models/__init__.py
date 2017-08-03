from app import db

class BaseMinin(db.Model):
    @classmethod
    def create(cls, **kwargs):
        recode = cls(**kwargs)
        db.session.add(recode)
        db.session.commit()
        return recode