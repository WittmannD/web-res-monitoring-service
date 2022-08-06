from dataclasses import dataclass
from datetime import datetime, timedelta
from http import HTTPStatus

from sqlalchemy import event, select, func, delete

from .BaseModel import BaseModel, db
from ..utils.utils import remove_overlimit

MAX_COUNT = 50


@dataclass
class MonitorRequestsModel(BaseModel):
    __tablename__ = 'monitor_requests'

    timestamp: datetime
    elapsed: timedelta
    status_code: HTTPStatus
    response: str
    monitor_id: int

    timestamp = db.Column(db.DateTime, nullable=False)
    elapsed = db.Column(db.Numeric, nullable=False)
    status_code = db.Column(db.Enum(HTTPStatus), nullable=False)
    response = db.Column(db.Text, nullable=False)
    monitor_id = db.Column(db.Integer, db.ForeignKey('monitors.id'), nullable=False)


@event.listens_for(MonitorRequestsModel, 'before_insert')
def receive_before_insert(mapper, connection, target):
    remove_overlimit(MAX_COUNT, mapper, connection, target, 'monitor_id')
