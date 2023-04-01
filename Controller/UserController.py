from fastapi import Depends, APIRouter
from Service.UserService import create_user, login, verify_token

user = APIRouter()


# register a new user
@user.post("/register", status_code=201)
def register(return_value: dict = Depends(create_user)):
    return return_value


# login
@user.post("/login", status_code=200)
def login(return_value: dict = Depends(login)):
    return return_value


@user.get("/verify", status_code=200)
def verify_token(return_value: dict = Depends(verify_token)):
    return return_value

