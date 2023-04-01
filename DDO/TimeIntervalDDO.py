from datetime import datetime

from pydantic import BaseModel


class TimeIntervalDDO(BaseModel):
    date: str
    time_interval_start: str
    time_interval_end: str


class TimeIntervalVerboseDDO(BaseModel):
    time_interval_id: int
    date: str
    time_interval_start: str
    time_interval_end: str


class TimeIntervalUpdateDDO(BaseModel):
    time_interval_id: int
    date: str
    time_interval_start: str
    time_interval_end: str
