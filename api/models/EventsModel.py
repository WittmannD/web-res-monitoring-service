from dataclasses import dataclass
from datetime import datetime, timedelta
from http import HTTPStatus

from sqlalchemy import event, select, func, delete

from .BaseModel import BaseModel, db
from ..utils.constants import MonitorStatus
from ..utils.utils import remove_overlimit

MAX_COUNT = 50


@dataclass
class EventsModel(BaseModel):
    __tablename__ = 'events'

    event: MonitorStatus
    reason: HTTPStatus
    datetime: datetime
    user_id: int
    monitor_id: int

    event = db.Column(db.Enum(MonitorStatus), nullable=False)
    reason = db.Column(db.Enum(HTTPStatus), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    monitor_id = db.Column(db.Integer, db.ForeignKey('monitors.id'), nullable=False)


@event.listens_for(EventsModel, 'before_insert')
def receive_before_insert(mapper, connection, target):
    remove_overlimit(MAX_COUNT, mapper, connection, target, 'monitor_id')
