from fastapi import APIRouter, Depends

from Service.AvailableTimeService import create_availability, get_user_availability
from Service.TimeService import get_time_interval, create_time_interval, update_time_interval

time = APIRouter()


@time.get("/time_interval", status_code=200)
def get_time_interval(return_value: dict = Depends(get_time_interval)):
    return return_value


@time.post("/time_interval", status_code=200)
def create_time_interval(return_value: dict = Depends(create_time_interval)):
    return return_value


@time.put("/time_interval_update", status_code=200)
def update_time_interval(return_value: dict = Depends(update_time_interval)):
    return return_value


@time.get("/availability", status_code=200)
def create_availability_time_interval(return_value: dict = Depends(get_user_availability)):
    return return_value


@time.post("/availability", status_code=200)
def create_availability_time_interval(return_value: dict = Depends(create_availability)):
    return return_value
