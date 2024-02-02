import json
import uuid
from datetime import datetime, date
from enum import Enum

from sqlalchemy import event, DDL, inspect
from flask_sqlalchemy import SQLAlchemy
from slugify import slugify

from src.extensions import db


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
    def count_by(cls, stmt):
        return cls.query.filter(stmt).count()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def find_latest(cls):
        return cls.query.order_by(cls.created_at.desc()).first()

    @classmethod
    def find_by_first(cls, stmt=True, **kwargs):
        return cls.query.filter(stmt).filter_by(**kwargs).first()

    @classmethod
    def find_by(cls, stmt=True, **kwargs):
        return cls.query.filter(stmt).filter_by(**kwargs).all()

    @classmethod
    def find_and_order_by(cls, stmt=True, order_by=None, **kwargs):
        order_by = order_by or dict(created_at='desc')
        ordering = [
            getattr(getattr(cls, field, cls.created_at), direction, field.desc)()
            for field, direction in order_by.items()
        ]

        return cls.query.filter(stmt).filter_by(**kwargs).order_by(*ordering).all()

    @classmethod
    def find_paginate_and_order_by(cls, page=1, per_page=10, order_by=None, stmt=True, **kwargs):
        if order_by is None:
            order_by = ['created_at desc']

        ordering = []
        for parameter in order_by:
            [field, direction] = parameter.split(' ')

            field = getattr(cls, field, cls.created_at)
            direction = getattr(field, direction, field.desc)
            ordering.append(direction())

        return cls.query.filter(stmt).filter_by(**kwargs).order_by(*ordering).paginate(page=page, per_page=per_page,
                                                                                       error_out=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def as_json_serializable(self):
        def json_serial(obj):
            """JSON serializer for objects not serializable by default json code"""

            if isinstance(obj, (datetime, date)):
                return obj.isoformat()

            if isinstance(obj, Enum):
                return obj.value

            raise TypeError("Type %s not serializable" % type(obj))

        return json.loads(json.dumps(self.as_dict(), indent=4, sort_keys=True, default=json_serial))

    """ Utility functions """

    @classmethod
    def make_slug(cls, slug):
        return slugify(slug)

    @classmethod
    def date_to_string(cls, raw_date):
        return "{}".format(raw_date)


@event.listens_for(BaseModel, 'before_insert', propagate=True)
def before_insert(mapper, connection, instance):
    instance.created_at = datetime.utcnow()


@event.listens_for(BaseModel, 'before_update', propagate=True)
def before_update(mapper, connection, instance):
    instance.updated_at = datetime.utcnow()
