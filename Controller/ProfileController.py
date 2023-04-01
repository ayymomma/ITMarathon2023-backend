from fastapi import APIRouter, Depends

from Service.ProfileService import get_profile, update_personal_profile

profile = APIRouter()


@profile.get("/profile", status_code=200)
def get_profile(return_value: dict = Depends(get_profile)):
    return return_value


@profile.put("/profile_update", status_code=200)
def update_profile(return_value: dict = Depends(update_personal_profile)):
    return return_value
