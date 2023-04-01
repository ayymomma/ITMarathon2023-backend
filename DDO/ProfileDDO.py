from pydantic import BaseModel


class ProfileDDO(BaseModel):
    first_name: str
    last_name: str
    dept: str
    office_name: str
    team_name: str
    floor_number: str


class ProfileUpdateDDO(BaseModel):
    first_name: str
    last_name: str
    dept: str
    office_name: str
    team_name: str
    floor_number: str

