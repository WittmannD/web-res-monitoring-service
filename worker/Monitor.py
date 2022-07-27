import traceback
from datetime import datetime, timedelta
from http import HTTPStatus

import aiohttp

from api.models import MonitorRequestsModel
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
            status_code=HTTPStatus(response.status).name,
            response=await response.text(),
            monitor_id=self.model.id
        )
        response.raise_for_status()

    async def check(self):
        monitor_status = MonitorStatus.DOWN.name

        try:
            self.request_timestamp = datetime.utcnow()
            await HttpClient.request(
                self.model.method.name.lower(),
                self.model.url,
                None,
                self.set_request_data
            )

        except aiohttp.ClientResponseError as err:
            pass

        except Exception as err:
            print(err)
            print(traceback.format_exc())
            raise err

        else:
            monitor_status = MonitorStatus.UP.name

        finally:
            monitor_request = MonitorRequestsModel(**self.request_data)
            self.model.status = monitor_status
            self.model.next_check_at = round_time_to_minutes(
                self.model.next_check_at + timedelta(minutes=float(self.model.interval)),
                base_minutes=CHECK_EVERY_MINUTES
            )

            DB.session.add(monitor_request)
            DB.session.add(self.model)

        print(datetime.utcnow(), self.model.url, self.request_data['status_code'], self.request_data['elapsed'],
              sep='\t', end='\n\n')
