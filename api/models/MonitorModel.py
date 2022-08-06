from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import event, select

from .BaseModel import BaseModel, db
from ..utils.constants import HttpMethod, MonitorStatus
from ..utils.utils import round_time_to_minutes


def get_dispatch_time(context):
    interval = context.get_current_parameters().get('interval')
    return round_time_to_minutes(datetime.utcnow() + timedelta(minutes=float(interval)), 5)


@dataclass
class MonitorModel(BaseModel):
    __tablename__ = 'monitors'

    url: str
    method: HttpMethod
    running: bool
    status: Optional[MonitorStatus]
    interval: int
    next_check_at: Optional[datetime]
    user_id: int

    url = db.Column(db.String, nullable=False)
    method = db.Column(db.Enum(HttpMethod), nullable=False)
    running = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.Enum(MonitorStatus), default=MonitorStatus.UP.value)
    interval = db.Column(db.Integer, nullable=False)
    next_check_at = db.Column(db.DateTime, default=get_dispatch_time)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


@event.listens_for(MonitorModel, 'before_update')
def update_dispatch_time(mapper, connection, target):
    interval = target.interval
    setattr(target, 'next_check_at', round_time_to_minutes(datetime.utcnow() + timedelta(minutes=float(interval)), 5))
