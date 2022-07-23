from enum import Enum, unique


MONITORING_ROUTE = '/monitoring'
SINGLE_MONITOR_ROUTE = '/monitoring/<monitor_id>'
LOGIN_ROUTE = '/auth/login'
SIGNUP_ROUTE = '/auth/signup'
AUTH_CHECK_ROUTE = '/auth/check'


@unique
class HttpMethod(Enum):
    GET = 0
    POST = 1
    OPTIONS = 2
