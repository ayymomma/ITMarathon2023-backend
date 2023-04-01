from pydantic import BaseModel

from DDO.TimeIntervalDDO import TimeIntervalDDO, TimeIntervalVerboseDDO


class InvitationDDO(BaseModel):
    invite_id: int
    time_interval_id: int
    place: str
    comment: str


class InvitationRequestDDO(BaseModel):
    time_interval: TimeIntervalDDO
    place: str
    comment: str
    users: list[int]


class InvitationVerboseDDO(BaseModel):
    invite_id: int
    time_interval: TimeIntervalVerboseDDO
    place: str
    comment: str
    users: list[int]
