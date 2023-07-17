import random


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
