import traceback
from datetime import datetime
from http import HTTPStatus

import requests
from celery.utils.log import get_task_logger

from src.extensions import db
from src.models.EventsModel import EventsModel
from src.models.MonitorModel import MonitorModel
from src.models.MonitorRequestsModel import MonitorRequestsModel
from src.utils.HttpClient import HttpClient
from src.utils.constants import MonitorStatus, HttpMethod

task_logger = get_task_logger(__name__)


class Monitor:
    request_data: dict
    request_timestamp: datetime

    def __init__(self, data: dict):
        self.data = data

    def set_request_data(self, response: requests.Response):
        self.request_data = dict(
            timestamp=self.request_timestamp,
            elapsed=response.elapsed.total_seconds() * 1000.0,
            status_code=HTTPStatus(response.status_code),
            response=response.text,
            monitor_id=self.data.get('id')
        )
        response.raise_for_status()

    def check(self):
        monitor_status = MonitorStatus(self.data.get('status'))
        monitor_method = HttpMethod(self.data.get('method'))
        event_type = None

        try:
            self.request_timestamp = datetime.utcnow()
            HttpClient.request(
                method=self.data.get('method').lower(),
                url=self.data.get('url'),
                payload=None,  # Implement client payloads
                resolve=self.set_request_data
            )

        except (requests.RequestException, requests.HTTPError) as err:
            if monitor_status == MonitorStatus.UP:
                event_type = MonitorStatus.DOWN

            monitor_status = MonitorStatus.DOWN

        except Exception as err:
            monitor_status = MonitorStatus.DOWN
            task_logger.error(err)
            task_logger.debug(traceback.format_exc())
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
                    user_id=self.data.get('user_id'),
                    monitor_id=self.data.get('id')
                )
                db.session.add(event)

            monitor_request = MonitorRequestsModel(**self.request_data)
            self.data['status'] = monitor_status

            db.session.add(monitor_request)
            db.session.merge(MonitorModel(**self.data))

            db.session.commit()
            task_logger.info(f'request to {self.data.get("url")} succeeded. elapsed {self.request_data.get("elapsed")}ms')
