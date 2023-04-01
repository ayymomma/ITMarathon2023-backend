from datetime import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import Database.Models as models
from DDO.AvailableTimeDDO import AvailableTimeUserDDO, AvailableTimeDDO
from DDO.TimeIntervalDDO import TimeIntervalDDO, TimeIntervalVerboseDDO
from Service.TimeService import get_time_interval, create_time_interval, delete_time_interval

from Service.UserService import auth_handler, get_db
from Service.UtilsService import str_to_datetime, strip_datetime_to_date, date_to_string


def get_user_availability(user_id: int = Depends(auth_handler.auth_wrapper),
                          requested_user_id: int = None,
                          requested_date: str = None,
                          db: Session = Depends(get_db)):
    if requested_user_id is None or requested_user_id == "":
        requested_user_id = user_id
    if requested_date is None or requested_date == "":
        date_as_datetime = strip_datetime_to_date(datetime.now())
    else:
        try:
            date_as_datetime = str_to_datetime(requested_date)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Bad date format.')

    all_user_available_time_intervals = db.query(models.AvailableTime) \
        .filter(models.AvailableTime.user_id == requested_user_id)

    result: list[TimeIntervalVerboseDDO] = []
    for available_interval in all_user_available_time_intervals:
        interval = get_time_interval(time_interval_id=available_interval.time_interval_id, user_id=requested_user_id,
                                     db=db)

        # get only those intervals from this datetime.
        if interval.date == date_as_datetime:
            interval_ddo = TimeIntervalVerboseDDO(time_interval_id=interval.time_interval_id,
                                                  date=date_to_string(interval.date),
                                                  time_interval_start=interval.time_interval_start,
                                                  time_interval_end=interval.time_interval_end)
            result.append(interval_ddo)
    return AvailableTimeUserDDO(user_id=requested_user_id, time_intervals=result)


def create_availability(time_interval: TimeIntervalDDO, user_id: int = Depends(auth_handler.auth_wrapper),
                        db: Session = Depends(get_db)):
    # TODO: check for time to not intersect with other
    # create time_interval
    created_time_interval = create_time_interval(time_interval, user_id, db)

    # create availability for time interval
    created_availability = models.AvailableTime(user_id=user_id,
                                                time_interval_id=created_time_interval.time_interval_id)

    db.add(created_availability)
    db.commit()
    db.refresh(created_availability)

    time_interval_ddo = TimeIntervalDDO(date=date_to_string(created_time_interval.date),
                                        time_interval_start=created_time_interval.time_interval_start,
                                        time_interval_end=created_time_interval.time_interval_end)
    return AvailableTimeDDO(user_id=user_id, time_interval=time_interval_ddo)


def delete_availability(time_interval_id: int, user_id: int = Depends(auth_handler.auth_wrapper),
                        db: Session = Depends(get_db)):
    # check if that availability exists
    try:
        availability_interval = db.query(models.AvailableTime).filter(
            models.AvailableTime.user_id == user_id and models.AvailableTime.time_interval_id == time_interval_id) \
            .first()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Availability not found.')

    # delete availability
    db.query(models.AvailableTime).filter(models.AvailableTime.timeline_id == availability_interval.time_interval_id).delete()
    db.commit()

    # delete time_interval
    delete_time_interval(time_interval_id, user_id, db)
    return {"message": "Availability and associated time interval deleted successfully"}
