from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from Database.Database import Base


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


class UserProfile(Base):
    __tablename__ = "user_profile"
    profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    first_name = Column(String)
    last_name = Column(String)
    dept = Column(String)
    office_name = Column(String)
    team_name = Column(String)
    floor_number = Column(String)


class AvailableTime(Base):
    __tablename__ = "available_time"
    timeline_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    time_interval_id = Column(Integer, ForeignKey("time_interval.time_interval_id"))


class TimeInterval(Base):
    __tablename__ = "time_interval"
    time_interval_id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    time_interval_start = Column(String)
    time_interval_end = Column(String)
