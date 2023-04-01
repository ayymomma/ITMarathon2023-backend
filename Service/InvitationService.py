from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

import Database.Models as models
from DDO.InvitationDDO import InvitationRequestDDO, InvitationVerboseDDO
from DDO.TimeIntervalDDO import TimeIntervalVerboseDDO
from Service.ProfileService import get_profile
from Service.TimeService import create_time_interval, get_time_interval
from Service.UserService import get_db, auth_handler
from Service.UtilsService import date_to_string


def create_invitation(invitation: InvitationRequestDDO, user_id: int = Depends(auth_handler.auth_wrapper),
                      db: Session = Depends(get_db)):
    # create time interval
    time_interval = create_time_interval(invitation.time_interval, user_id, db)
    invitation_model = models.Invitation(time_interval_id=time_interval.time_interval_id, place=invitation.place,
                                         comment=invitation.comment)

    db.add(invitation_model)
    db.commit()
    db.refresh(invitation_model)

    time_interval_ddo = TimeIntervalVerboseDDO(time_interval_id=time_interval.time_interval_id,
                                               date=date_to_string(time_interval.date),
                                               time_interval_start=time_interval.time_interval_start,
                                               time_interval_end=time_interval.time_interval_end)
    invitation_ddo = InvitationVerboseDDO(invite_id=invitation_model.invite_id, time_interval=time_interval_ddo,
                                          place=invitation_model.place, comment=invitation_model.comment, users=[])

    # invite self
    add_user_to_invitation(invitation_model.invite_id, user_id, user_id, db)

    # Add every user from invitation
    for invited_user_id in invitation.users:
        try:
            add_user_to_invitation(invitation_model.invite_id, invited_user_id, user_id, db)
            invitation_ddo.users.append(invited_user_id)
        except Exception:
            # we will ignore the users that could not be added to an invite.
            pass

    return invitation_ddo


def get_invitation(invitation_id: int = None, user_id: int = Depends(auth_handler.auth_wrapper),
                   db: Session = Depends(get_db)):
    invitation_list = db.query(models.Invitation).filter(models.Invitation.invite_id == invitation_id).all()
    if len(invitation_list) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No invitation found.')

    result: list[InvitationVerboseDDO] = []
    for invitation in invitation_list:
        time_interval = get_time_interval(invitation.time_interval_id, user_id, db)
        time_interval_ddo = TimeIntervalVerboseDDO(time_interval_id=time_interval.time_interval_id,
                                                   date=date_to_string(time_interval.date),
                                                   time_interval_start=time_interval.time_interval_start,
                                                   time_interval_end=time_interval.time_interval_end)

        invited_users_request_list = get_invited_users(invitation_id, user_id, db)
        invited_users = list(map(lambda x: x.user_id, invited_users_request_list))

        invitation_ddo = InvitationVerboseDDO(invite_id=invitation.invite_id, time_interval=time_interval_ddo,
                                              place=invitation.place, comment=invitation.comment, users=invited_users)
        result.append(invitation_ddo)

    return result


def add_user_to_invitation(invitation_id: int, guest_id: int,
                           user_id: int = Depends(auth_handler.auth_wrapper),
                           db: Session = Depends(get_db)):
    # check if user exists
    try:
        get_profile(user_id=user_id, db=db, requested_user_id=guest_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    # check if invitation exists
    try:
        get_invitation(invitation_id=invitation_id, db=db)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')

    # check if user added already
    already_added = db.query(models.InvitationRequest).filter(models.InvitationRequest.invite_id == invitation_id and \
                                                              models.InvitationRequest.user_id == guest_id).all()
    if len(already_added) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already invited.')

    inviteRequest = models.InvitationRequest(invite_id=invitation_id, user_id=guest_id, status='Pending')
    db.add(inviteRequest)
    db.commit()
    db.refresh(inviteRequest)

    return inviteRequest


def get_invited_users(invitation_id: int, user_id: int = Depends(auth_handler.auth_wrapper),
                      db: Session = Depends(get_db)):
    return db.query(models.InvitationRequest).filter(models.InvitationRequest.invite_id == invitation_id).all()


def get_user_invitation_requests(user_id: int = Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    return db.query(models.InvitationRequest).filter(models.InvitationRequest.user_id == user_id).all()
