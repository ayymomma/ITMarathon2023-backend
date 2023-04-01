from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from Auth.AuthHandler import AuthHandler
from DDO.UserDDO import UserRegisterDDO, UserLoginDDO
from Database.Database import SessionLocal
import Database.Models as models

from Database.Database import engine

models.Base.metadata.create_all(bind=engine)
auth_handler = AuthHandler()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def email_exists(email: str, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.email == email).first() is not None


def create_user(user_register: UserRegisterDDO, db: Session = Depends(get_db)):
    if email_exists(user_register.email, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered",
                            )
    user_model = models.User(password=auth_handler.get_password_hash(user_register.password),
                             email=user_register.email)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    user_profile = models.UserProfile(user_id=user_model.user_id, first_name="dummy", last_name="dummy", dept="dummy",
                                      office_name="dummy", team_name="dummy", floor_number=0)

    db.add(user_profile)
    db.commit()
    db.refresh(user_profile)
    return {"message": "User created"}


def login(user_login: UserLoginDDO, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.email == user_login.email).first()
    if not user_model or not auth_handler.verify_password(user_login.password, user_model.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password",
                            )
    token = auth_handler.encode_token(user_model.user_id)
    return {"token": token}


def verify_token(user_id: int = Depends(auth_handler.auth_wrapper)):
    return {"message": "Token verified"}
