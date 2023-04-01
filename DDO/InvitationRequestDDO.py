from pydantic import BaseModel


class InvitationAssocDDO(BaseModel):
    invite_id: int
    user_id: int
    status: str
