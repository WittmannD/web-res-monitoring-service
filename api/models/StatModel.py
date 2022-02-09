from dataclasses import dataclass
from datetime import datetime

from .BaseModel import BaseModel, db


@dataclass
class StatModel(BaseModel):
    __tablename__ = 'stats'

    response_time: float
    timestamp: datetime
    status: bool
    monitor_id: int

    response_time = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=True)
    monitor_id = db.Column(db.Integer, db.ForeignKey('monitors.id'), nullable=False)

    """ Database operations """

    @classmethod
    def count_by(cls, **kwargs):
        cls.query.count(kwargs)
