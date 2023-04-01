from datetime import time, datetime, date


def is_time_interval_valid(time_start: str, time_end: str):
    return time_start <= time_end


def str_to_time(time_string: str) -> time:
    return datetime.strptime(time_string, '%H:%M').time()


def str_to_datetime(date_string: str) -> datetime:
    return datetime.strptime(date_string, '%d-%m-%Y')
