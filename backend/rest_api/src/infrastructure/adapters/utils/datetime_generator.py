from datetime import datetime
from zoneinfo import ZoneInfo

from src.domain.value_objects import Timestamp

from src.domain.ports import TimestampGenerator


class DatetimeGenerator(TimestampGenerator):
    def __call__(self) -> Timestamp:
        kyiv_tz = ZoneInfo("Europe/Kyiv")
        return Timestamp(datetime.now(kyiv_tz))
