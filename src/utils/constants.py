from enum import Enum, unique

API_PREFIX = '/api/v1'

MONITORING_ROUTE = '/monitoring'
SINGLE_MONITOR_ROUTE = '/monitoring/<int:monitor_id>'
MONITOR_REQUESTS_ROUTE = '/monitoring/<int:monitor_id>/requests'
EVENTS_ROUTE = '/monitoring/events'

LOGIN_ROUTE = '/auth/login'
SIGNUP_ROUTE = '/auth/signup'
SEND_EMAIL_ROUTE = '/auth/send-verification-email'
VERIFICATION_ROUTE = '/auth/verify-email'

USER_ROUTE = '/user'


@unique
class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    OPTIONS = 'OPTIONS'


@unique
class MonitorStatus(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
