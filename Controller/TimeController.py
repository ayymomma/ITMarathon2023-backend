from fastapi import APIRouter, Depends

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
