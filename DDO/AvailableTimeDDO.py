from pydantic import BaseModel

from DDO.TimeIntervalDDO import TimeIntervalDDO, TimeIntervalVerboseDDO


class AvailableTimeDDO(BaseModel):
    user_id: int
    time_interval: TimeIntervalDDO


class AvailableTimeUserDDO(BaseModel):
    user_id: int
    time_intervals: list[TimeIntervalVerboseDDO]
