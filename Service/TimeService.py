from datetime import datetime, time

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import Database.Models as models
from DDO.TimeIntervalDDO import TimeIntervalDDO, TimeIntervalUpdateDDO

from Service.UserService import auth_handler, get_db
from Service.UtilsService import is_time_interval_valid, str_to_datetime


def get_time_interval(time_interval_id: int = None, user_id: int = Depends(auth_handler.auth_wrapper),
                      db: Session = Depends(get_db)):
    if time_interval_id is None:
        time_interval = db.query(models.TimeInterval).all()
    else:
        time_interval = db.query(models.TimeInterval).filter(
            models.TimeInterval.time_interval_id == time_interval_id).first()

    return time_interval


def create_time_interval(time_interval: TimeIntervalDDO, user_id: int = Depends(auth_handler.auth_wrapper),
                         db: Session = Depends(get_db)):
    # time_start = datetime.now().time()  # str_to_time(time_interval.time_interval_start)
    # time_end = datetime.now().time()  # str_to_time(datetime)
    try:
        # checks if start is less than end
        time_start = time_interval.time_interval_start
        time_end = time_interval.time_interval_end
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Bad time format.')

    if not is_time_interval_valid(time_start, time_end):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Time interval start time must be less than end time.')

    created_interval = models.TimeInterval(date=str_to_datetime(datetime.now().strftime("%d-%m-%Y")),
                                           time_interval_start=time_start,
                                           time_interval_end=time_end)

    if time_interval.date != "":
        try:
            created_interval.date = str_to_datetime(time_interval.date)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Bad date format.')

    db.add(created_interval)
    db.commit()
    db.refresh(created_interval)
    return created_interval


def update_time_interval(time_interval_update: TimeIntervalUpdateDDO, user_id: int = Depends(auth_handler.auth_wrapper),
                         db: Session = Depends(get_db)):
    try:
        time_interval = db.query(models.TimeInterval).filter(
            models.TimeInterval.time_interval_id == time_interval_update.time_interval_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='There is no time interval with the provided id.')

    # verify each field is not None
    # TODO: Validate time format.
    if time_interval_update.date is not None:
        try:
            time_interval.date = str_to_datetime(time_interval_update.date)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Bad date format.')
    if time_interval_update.time_interval_start is not None and time_interval_update.time_interval_start != "":
        time_interval.time_interval_start = time_interval_update.time_interval_start
    if time_interval_update.time_interval_end is not None and time_interval_update.time_interval_end != "":
        time_interval.time_interval_end = time_interval_update.time_interval_end

    if not is_time_interval_valid(time_interval.time_interval_start, time_interval.time_interval_end):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Time interval start time must be less than end time.')

    db.commit()
    db.refresh(time_interval)
    return {"message": "Time interval updated successfully"}
