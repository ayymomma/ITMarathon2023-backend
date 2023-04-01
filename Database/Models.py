from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from Database.Database import Base


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

