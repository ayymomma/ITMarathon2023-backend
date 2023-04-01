from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from DataBase.Database import Base


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


class Subscription(Base):
    __tablename__ = "subscription"
    subscription_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    subscription_state = Column(String)
    subscription_name = Column(String)
    subscription_date = Column(DateTime)
    subscription_end_date = Column(DateTime)
