import traceback
from datetime import datetime, timedelta
from http import HTTPStatus

import aiohttp

from api.models import MonitorRequestsModel
from api.models.EventsModel import EventsModel
from api.utils.constants import MonitorStatus
from worker.HttpClient import HttpClient
from worker.db import DB
from worker.utils import round_time_to_minutes

CHECK_EVERY_MINUTES = 5


class Monitor:
    def __init__(self, model):
        self.model = model
        self.request_data = dict()
        self.request_timestamp = None

    async def set_request_data(self, response: aiohttp.ClientResponse):
        self.request_data = dict(
            timestamp=self.request_timestamp,
            elapsed=(datetime.utcnow() - self.request_timestamp).total_seconds(),
            status_code=HTTPStatus(response.status),
            response=await response.text(),
            monitor_id=self.model.id
        )
        response.raise_for_status()

    async def check(self):
        monitor_status = self.model.status
        event_type = None

        try:
            self.request_timestamp = datetime.utcnow()
            await HttpClient.request(
                method=self.model.method.name.lower(),
                url=self.model.url,
                payload=None,
                resolve=self.set_request_data
            )

        except aiohttp.ClientResponseError as err:
            if monitor_status == MonitorStatus.UP:
                event_type = MonitorStatus.DOWN

            monitor_status = MonitorStatus.DOWN

        except Exception as err:
            monitor_status = MonitorStatus.DOWN
            print(err)
            print(traceback.format_exc())
            raise err

        else:
            if monitor_status == MonitorStatus.DOWN:
                event_type = MonitorStatus.UP

            monitor_status = MonitorStatus.UP

        finally:
            if event_type is not None:
                event = EventsModel(
                    datetime=self.request_timestamp,
                    event=event_type,
                    reason=self.request_data.get('status_code'),
                    user_id=self.model.user_id,
                    monitor_id=self.model.id
                )
                DB.session.add(event)

            monitor_request = MonitorRequestsModel(**self.request_data)
            self.model.status = monitor_status

            DB.session.add(monitor_request)
            DB.session.add(self.model)

        print(datetime.utcnow(), self.model.url, self.request_data['status_code'], self.request_data['elapsed'],
              sep='\t', end='\n\n')
