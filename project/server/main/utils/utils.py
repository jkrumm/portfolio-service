import os

from nomics import Nomics


def get_nomics():
    return Nomics(os.environ.get('NOMICS_KEY'))


def percentage(one, two):
    if (one and two and float(one) > 0.0 and float(two) > 0.0):
        return round((float(one) / float(two) - 1) * 100, 2)
    else:
        return None


def f(string):
    if string:
        f = float(string)
        if f > 100000:
            return int(f)
        else:
            return round(f, 2)
    else:
        return None
