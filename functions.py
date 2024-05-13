import datetime
import uuid
from typing import List

from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
time_zone = os.getenv('TIME_ZONE')
hours_array = ["16:00", "17:00", "18:00"]
day_map = {
    "monday": 0, "mon": 0, "lunes": 0, "lun": 0, "l": 0, "m": 0,
    "tuesday": 1, "tue": 1, "martes": 1, "mar": 1, "m": 1, "t": 1,
    "wednesday": 2, "wed": 2, "miércoles": 2, "miercoles": 2, "mié": 2, "mie": 2, "x": 2, "w": 2,
    "thursday": 3, "thu": 3, "jueves": 3, "jue": 3, "j": 3, "th": 3,
    "friday": 4, "fri": 4, "viernes": 4, "vie": 4, "v": 4, "f": 4,
    "saturday": 5, "sat": 5, "sábado": 5, "sabado": 5, "sáb": 5, "sab": 5, "sa": 5, "s": 5,
    "sunday": 6, "sun": 6, "domingo": 6, "dom": 6, "d": 6, "su": 6
}


def get_hours_array():
    return hours_array


def get_utc_hours_array():
    utc_hours_array = []
    for hour in hours_array:
        utc_hours_array.append(hour + int(time_zone))
    return utc_hours_array


def check_days(days):
    days = days.split(",")
    for day in days:
        if day not in day_map:
            return False
    return True
def check_hours(hours):
    hours = hours.split(",")
    for hour in hours:
        if len(hour.split(":")) != 2:
            return False
        if not hour.split(":")[0].isdigit() or not hour.split(":")[1].isdigit():
            return False
        if int(hour.split(":")[0]) < 0 or int(hour.split(":")[0]) > 23:
            return False
        if int(hour.split(":")[1]) < 0 or int(hour.split(":")[1]) > 59:
            return False
    return True


def get_days(days):
    days = days.split(",")
    for i in range(len(days)):
        days[i] = day_map[days[i]]
    return days

def get_min_hour(hours):
    min_hour = 24
    for hour in hours:
        if int(hour.split(":")[0]) < min_hour:
            min_hour = int(hour.split(":")[0])
    return min_hour

def get_timestamps(day, hours,force_next_week=False):
    timestamps = {}
    minhour = get_min_hour(hours)
    for timestamp in hours:
        hour = int(timestamp.split(":")[0])
        minute = int(timestamp.split(":")[1])
        date = datetime.datetime.now()
        if date.weekday() == day:
            if force_next_week:
                date += datetime.timedelta(days=7)
            if date.hour < minhour:
                date = date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            else:
                date = date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                date += datetime.timedelta(days=(7 - date.weekday() + day) % 7)
        else:
            date = date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            date += datetime.timedelta(days=(7 - date.weekday() + day) % 7)

        date_string = date.strftime("%Y-%m-%d %H:%M:%S")
        datetime_string = date.strftime("%Y-%m-%d %H:%M:%S")
        timestamps[date_string] = datetime_string
    return timestamps


def get_discord_timestamps(strdatetime, force_next_week=False):
    date = datetime.datetime.strptime(strdatetime, "%Y-%m-%d %H:%M:%S")

    date_formated = f"<t:{int(date.timestamp())}:R>"
    return date_formated


def get_timestamps_map(days, hours, force_next_week=False):
    timestamps_map = {}
    for day in days:
        timestamps_map.update(get_timestamps(day,hours ,force_next_week))
    return timestamps_map


def transform_strdays_to_timestamps(days: str, force_next_week: bool = False, hours: List[str] = None):
    if hours is None:
        hours = get_hours_array()
    if not check_days(days):
        return "Invalid days"
    days = get_days(days)
    return get_timestamps_map(days, hours, force_next_week)


def generate_uuid():
    return str(uuid.uuid4())


# print(transform_strdays_to_timestamps("l,m,x", force_next_week=True))
