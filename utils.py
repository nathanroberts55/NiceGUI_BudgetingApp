import random
from datetime import datetime, timedelta


def okay(message, *args):
    print("[+]", message, *args)


def warn(message, *args):
    print("[*]", message, *args)


def error(message, *args):
    print("[-]", message, *args)


def generate_random_float():
    num = round(random.uniform(10, 200), 2)
    return str(num)


def to_dict(objects):
    dicts = []
    for obj in objects:
        dicts.append(dict(obj))
    return dicts


def enable_next(ui_element) -> None:
    return ui_element.enable()


def parse_date(date_string: str) -> datetime:
    formats = ["%Y-%m-%d", "%m/%d/%y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            pass
    raise ValueError(
        f"time data {date_string!r} does not match any of the supported formats"
    )


def get_current_month() -> (str, str, str):
    # Get the current date
    now = datetime.now()
    # Calculate the first day of the current month
    first_day = now.replace(day=1)
    # Calculate the last day of the current month
    last_day = (first_day + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    now = now.strftime("%m/%d/%y")
    first_day = first_day.strftime("%m/%d/%y")
    last_day = last_day.strftime("%m/%d/%y")

    return now, first_day, last_day
