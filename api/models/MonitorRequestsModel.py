from dataclasses import dataclass
from datetime import datetime, timedelta
from http import HTTPStatus

from sqlalchemy import event, select, func, delete

from .BaseModel import BaseModel, db


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
    count = (
        connection
        .scalar(select(func.count()).select_from(mapper))
    )

    if count > MAX_COUNT:
        connection.execute(
            delete(mapper)
            .where(
                mapper.c.id.in_(
                    select(mapper.c.id)
                    .order_by(mapper.c.created_at.asc()).limit(count - MAX_COUNT + 1)
                )
            )
        )
