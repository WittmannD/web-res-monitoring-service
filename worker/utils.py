from datetime import datetime, timedelta
import math


def ceil_round_to_base(n, base: int):
    return base * math.ceil(n / base)


def round_to_base(n, base: int):
    return base * round(n / base)


def round_time_to_minutes(dt: datetime, base_minutes: int) -> datetime:
    return dt.replace(minute=0, second=0) + timedelta(minutes=round_to_base(dt.minute, base_minutes))
