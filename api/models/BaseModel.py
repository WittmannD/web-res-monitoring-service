from datetime import datetime

from sqlalchemy import event
from flask_sqlalchemy import SQLAlchemy
from slugify import slugify

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    """ Database operations """

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def count_all(cls):
        return cls.query.count()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def find_latest(cls):
        return cls.query.order_by(cls.id.desc()).first()

    @classmethod
    def find_by_first(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def find_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def find_and_order_by(cls, order_by='id', **kwargs):
        return cls.query.filter_by(**kwargs).order_by(order_by).all()

    @classmethod
    def find_and_paginated_order_by(cls, page=1, per_page=10, order_by='created_at desc', **kwargs):
        field, direction = order_by.split(' ')
        field = getattr(cls, field, cls.id)
        order_by = getattr(field, direction, field.desc)()
        return cls.query.filter_by(**kwargs).order_by(order_by).paginate(page, per_page, error_out=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    """ Utility functions """

    @classmethod
    def make_slug(cls, slug):
        return slugify(slug)

    @classmethod
    def date_to_string(cls, raw_date):
        return "{}".format(raw_date)


@event.listens_for(BaseModel, 'before_insert', propagate=True)
def before_insert(mapper, connecton, instance):
    instance.created_at = datetime.utcnow()


@event.listens_for(BaseModel, 'before_update', propagate=True)
def before_update(mapper, connecton, instance):
    instance.updated_at = datetime.utcnow()
