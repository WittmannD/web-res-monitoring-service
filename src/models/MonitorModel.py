from __future__ import annotations

import math
from typing import Optional

from dataclasses import dataclass
from datetime import datetime, timedelta
from sqlalchemy import event, select, and_

from .BaseModel import BaseModel
from src.extensions import db
from src.utils.constants import HttpMethod, MonitorStatus
from src.utils.utils import round_time_to_minutes


def get_dispatch_time(context):
    interval = context.get_current_parameters().get('interval')
    return round_time_to_minutes(datetime.utcnow() + timedelta(minutes=float(interval)), 5)


@dataclass
class MonitorModel(BaseModel):
    __tablename__ = 'monitors'

    url: str = db.Column(db.String, nullable=False)
    method: HttpMethod = db.Column(db.Enum(HttpMethod), nullable=False)
    running: bool = db.Column(db.Boolean, nullable=False)
    status: Optional[MonitorStatus] = db.Column(db.Enum(MonitorStatus), default=MonitorStatus.UP.value)
    interval: int = db.Column(db.Integer, nullable=False)
    next_check_at: Optional[datetime] = db.Column(db.DateTime, default=get_dispatch_time)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @classmethod
    def get_pending(cls, period) -> list[MonitorModel]:
        now = datetime.utcnow()
        from_time, to_time = (
            now - timedelta(seconds=math.floor(period / 2)),
            now + timedelta(seconds=math.ceil(period / 2))
        )

        query = cls.query.filter(
            and_(
                cls.next_check_at >= from_time,
                cls.next_check_at <= to_time,
                cls.running
            )
        )

        return query.all()


@event.listens_for(MonitorModel, 'before_update')
def update_dispatch_time(mapper, connection, target):
    interval = target.interval
    setattr(target, 'next_check_at', round_time_to_minutes(datetime.utcnow() + timedelta(minutes=float(interval)), 5))
