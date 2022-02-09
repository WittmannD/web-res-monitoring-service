from enum import Enum, unique


@unique
class Method(Enum):
    GET = 0
    POST = 1
    OPTIONS = 2
