from fastapi import Depends, APIRouter

from Service.InvitationService import create_invitation, get_invitation, add_user_to_invitation, get_invited_users, \
    get_user_invitation_requests

invitation = APIRouter()


@invitation.get("/", status_code=200)
def get_invitation(return_value: dict = Depends(get_invitation)):
    return return_value


@invitation.post("/", status_code=200)
def create_invitation(return_value: dict = Depends(create_invitation)):
    return return_value


@invitation.get("/invited", status_code=200)
def get_users_invited_to_break(return_value: dict = Depends(get_invited_users)):
    return return_value


@invitation.get("/user", status_code=200)
def get_all_user_break_invitations(return_value: dict = Depends(get_user_invitation_requests)):
    return return_value


@invitation.post("/invite_user", status_code=200)
def add_user_to_invitation(return_value: dict = Depends(add_user_to_invitation)):
    return return_value


