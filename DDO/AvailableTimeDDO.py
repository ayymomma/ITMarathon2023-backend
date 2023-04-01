from pydantic import BaseModel

from DDO.TimeIntervalDDO import TimeIntervalDDO


class AvailableTimeDDO(BaseModel):
    time_interval_list: list[TimeIntervalDDO]