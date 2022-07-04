import argparse
import datetime
import logging
import os


def strip_quotes(origin: str) -> str:
    return origin.strip('\"').strip('\'')


def string_to_path(origin: str) -> str:
    expanded_origin = os.path.expanduser(origin)
    return strip_quotes(expanded_origin)


def string_to_loglevel(origin: str) -> int:
    string = origin.upper()
    if string == "WARN" or string == "WARNING":
        value = logging.WARN
    elif string == "INFO":
        value = logging.INFO
    elif string == "DEBUG":
        value = logging.DEBUG
    elif string == "ERROR" or string == "ERR":
        value = logging.ERROR
    else:
        raise argparse.ArgumentTypeError(f'Unknown {origin}, known values are WARN, INFO, DEBUG, ERROR')
    return value


def string_to_bool(origin: str) -> bool:
    if origin.upper() in ["Y", "YES", "YE"]:
        return True
    elif origin.upper() in ["N", "NO", "NOPE"]:
        return False
    else:
        raise RuntimeError(f"Can not convert {origin} to boolean")


def filebytes_to_human_size(size: int) -> str:
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    # bytes pretty-printing
    units_mapping = [
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'KB'),
        (1, 'b'),
    ]
    for factor, suffix in units_mapping:
        if size >= factor:
            amount = int(size / factor)
            return str(amount) + suffix


def float_to_date(seconds: float) -> datetime:
    return datetime.datetime.utcfromtimestamp(seconds)
