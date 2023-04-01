from fastapi import APIRouter, Depends

from Service.ProfileService import get_profile, update_personal_profile, get_all_users, search_profile_by_string

profile = APIRouter()


@profile.get("/profile", status_code=200)
def get_profile(return_value: dict = Depends(get_profile)):
    return return_value


@profile.get("/users", status_code=200)
def get_all_users(return_value: dict = Depends(get_all_users)):
    return return_value


@profile.get("/search", status_code=200)
def search_string(return_value: dict = Depends(search_profile_by_string)):
    return return_value


@profile.put("/profile_update", status_code=200)
def update_profile(return_value: dict = Depends(update_personal_profile)):
    return return_value
