import datetime
import uuid

from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
time_zone = os.getenv('TIME_ZONE')
hours_array = [16, 17, 18]
day_map = {
    "monday": 0, "mon": 0, "lunes": 0, "lun": 0, "l": 0, "m": 0,
    "tuesday": 1, "tue": 1, "martes": 1, "mar": 1, "m": 1, "t": 1,
    "wednesday": 2, "wed": 2, "miércoles": 2, "miercoles": 2, "mié": 2, "mie": 2, "x": 2, "w": 2,
    "thursday": 3, "thu": 3, "jueves": 3, "jue": 3, "j": 3, "th": 3,
    "friday": 4, "fri": 4, "viernes": 4, "vie": 4, "v": 4, "f": 4,
    "saturday": 5, "sat": 5, "sábado": 5, "sabado": 5, "sáb": 5, "sab": 5, "sa": 5,"s": 5,
    "sunday": 6, "sun": 6, "domingo": 6, "dom": 6, "d": 6, "su": 6
}


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


def get_days(days):
    days = days.split(",")
    for i in range(len(days)):
        days[i] = day_map[days[i]]
    return days


def get_timestamps(day,force_next_week=False):
    timestamps = {}
    for hour in get_utc_hours_array():
        date = datetime.datetime.now()
        if date.weekday() == day:
            if force_next_week:
                date += datetime.timedelta(days=7)
            if date.hour < 17:
                date = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            else:
                date = date.replace(hour=hour, minute=0, second=0, microsecond=0)
                date += datetime.timedelta(days=(7 - date.weekday() + day) % 7)
        else:
            date = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            date += datetime.timedelta(days=(7 - date.weekday() + day) % 7)

        date_string = date.strftime("%Y-%m-%d %H:%M:%S")
        datetime_string = date.strftime("%Y-%m-%d %H:%M:%S UTC"+str(time_zone))
        timestamps[date_string] = datetime_string
    return timestamps

def get_discord_timestamps(day, force_next_week=False):
    timestamps = {}
    for hour in get_utc_hours_array():
        date = datetime.datetime.now()
        if date.weekday() == day:
            if force_next_week:
                date += datetime.timedelta(days=7)
            if date.hour < 17:
                date = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            else:
                date = date.replace(hour=hour, minute=0, second=0, microsecond=0)
                date += datetime.timedelta(days=(7 - date.weekday() + day) % 7)
        else:
            date = date.replace(hour=hour, minute=0, second=0, microsecond=0)
            date += datetime.timedelta(days=(7 - date.weekday() + day) % 7)

        date_string = date.strftime("%Y-%m-%d %H:%M:%S")
        date_formated = f"<t:{int(date.timestamp())}:R>"
        timestamps[date_string] = date_formated
    return timestamps

def get_timestamps_map(days, force_next_week=False):
    timestamps_map = {}
    for day in days:
        timestamps_map.update(get_timestamps(day, force_next_week))
    return timestamps_map


def transform_strdays_to_timestamps(str_days, force_next_week=False):
    if not check_days(str_days):
        return "Invalid days"
    days = get_days(str_days)
    return get_timestamps_map(days, force_next_week)

def generate_uuid():
    return str(uuid.uuid4())

print(transform_strdays_to_timestamps("l,m,x", force_next_week=True))