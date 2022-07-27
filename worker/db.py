import math
import os
from datetime import datetime, timedelta

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import orm, and_
from sqlalchemy.ext.automap import automap_base

from api.models import MonitorModel, MonitorRequestsModel

MAX_REQUESTS = 50
load_dotenv()


class DB:
    base = automap_base()
    engine = sqlalchemy.create_engine(os.environ.get("DATABASE_URL"))
    base.prepare(autoload_with=engine, reflect=True)
    session = orm.Session(bind=engine)

    # MonitorModel = base.classes.monitors
    MonitorQuery = session.query(MonitorModel)

    # MonitorRequestsModel = base.classes.monitor_requests
    MonitorRequestsQuery = session.query(MonitorRequestsModel)

    @classmethod
    def fetch_monitors(cls, period):
        now = datetime.utcnow()
        from_time, to_time = (
            now - timedelta(seconds=math.floor(period / 2)),
            now + timedelta(seconds=math.ceil(period / 2))
        )

        query = cls.MonitorQuery.filter(
            and_(
                MonitorModel.next_check_at >= from_time,
                MonitorModel.next_check_at <= to_time
            )
        )

        return query.all()

    @classmethod
    def commit(cls):
        cls.session.commit()
