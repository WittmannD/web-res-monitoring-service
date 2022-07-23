from dataclasses import dataclass
from datetime import datetime

from .BaseModel import BaseModel, db
from ..utils.constants import HttpMethod


@dataclass
class MonitorModel(BaseModel):
    __tablename__ = 'monitors'

    url: str
    method: HttpMethod
    interval: int
    next_check_at: datetime
    user_id: int

    url = db.Column(db.String, nullable=False)
    method = db.Column(db.Enum(HttpMethod), nullable=False)
    interval = db.Column(db.Integer, nullable=False)
    next_check_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    """ Database operations """

    @classmethod
    def find_and_paginated_order_by(cls, page=1, per_page=10, order_by='created_at desc', **kwargs):
        field, direction = order_by.split(' ')
        field = getattr(cls, field, cls.id)
        order_by = getattr(field, direction, field.desc)()
        return cls.query.filter_by(**kwargs).order_by(order_by).paginate(page, per_page, error_out=False)
