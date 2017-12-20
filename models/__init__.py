from app import db


class Base:
    @classmethod
    def save(cls, record):
        db.session.add(record)
        db.session.commit()
        return record

    @classmethod
    def find(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    @classmethod
    def first(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get(cls, id):
        # http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session.expire_all
        # db.session.expire_all()
        return cls.query.get(id)

    @classmethod
    def get_or_404(cls, id):
        cls.query.get_or_404(id)

    @classmethod
    def count(cls, **kwargs):
        return cls.query.filter_by(**kwargs).count()

    @classmethod
    def all(cls, offset=None, limit=None, order_by=None, desc=False):
        query = cls.query
        if order_by is not None:
            if desc:
                query = query.order_by(db.desc(order_by))
            else:
                query = query.order_by(order_by)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    @classmethod
    def create(cls, **kwargs):
        return cls.save(cls(**kwargs))

    @classmethod
    def update(cls, record, **kwargs):
        for k, v in kwargs.items():
            setattr(record, k, v)
        db.session.commit()
        return record

    @classmethod
    def delete(cls, record, **kwargs):
        "It's danger"
        db.session.delete(record)
        db.session.commit()

    @classmethod
    def session_commit(cls):
        db.session.commit()

    def __del__(self):
        db.session.close()


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())
