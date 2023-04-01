from fastapi import Depends
from sqlalchemy.orm import Session
import Database.Models as models
from DDO.ProfileDDO import ProfileUpdateDDO
from Service.UserService import auth_handler, get_db


def get_profile(user_id: int = Depends(auth_handler.auth_wrapper),
                db: Session = Depends(get_db),
                requested_user_id: int = None):
    if requested_user_id is None:
        requested_user_id = user_id

    user_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == requested_user_id).first()

    return user_profile


def update_personal_profile(user_update: ProfileUpdateDDO, user_id: int = Depends(auth_handler.auth_wrapper),
                            db: Session = Depends(get_db)):
    user_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    # verify each field is not None
    if user_update.first_name is not None:
        user_profile.first_name = user_update.first_name
    if user_update.last_name is not None:
        user_profile.last_name = user_update.last_name
    if user_update.dept is not None:
        user_profile.dept = user_update.dept
    if user_update.office_name is not None:
        user_profile.office_name = user_update.office_name
    if user_update.team_name is not None:
        user_profile.team_name = user_update.team_name
    if user_update.floor_number is not None:
        user_profile.floor_number = user_update.floor_number
    db.commit()
    db.refresh(user_profile)
    return {"message": "Profile updated successfully"}
