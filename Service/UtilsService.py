from datetime import time, datetime


def is_time_interval_valid(time_start: str, time_end: str):
    return time_start <= time_end


def str_to_time(time_string: str) -> time:
    return datetime.strptime(time_string, '%H:%M').time()


def str_to_datetime(date_string: str) -> datetime:
    return datetime.strptime(date_string, '%d-%m-%Y')


def strip_datetime_to_date(date_time_obj: datetime) -> datetime:
    return str_to_datetime(date_time_obj.strftime("%d-%m-%Y"))


def date_now_string():
    return str_to_datetime(datetime.now().strftime("%d-%m-%Y"))


def date_to_string(input: datetime):
    return input.strftime("%d-%m-%Y")
