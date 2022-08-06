from enum import Enum, unique

MONITORING_ROUTE = '/monitoring'
SINGLE_MONITOR_ROUTE = '/monitoring/<int:monitor_id>'
MONITOR_REQUESTS_ROUTE = '/monitoring/<int:monitor_id>/requests'
EVENTS_ROUTE = '/monitoring/events'
LOGIN_ROUTE = '/auth/login'
SIGNUP_ROUTE = '/auth/signup'
AUTH_CHECK_ROUTE = '/auth/check'


@unique
class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    OPTIONS = 'OPTIONS'


@unique
class MonitorStatus(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
