#%%
from datetime import datetime as dt
from datetime import timedelta
from typing import Dict

from api.src.utils.logger import logger


def date_calc(date: dt, delta: int, timedelta=timedelta) -> str:
    """A function that applies a timedelta to an datetime object

    Args:
        date (datetime): An datetime in utc
        delta (int):the time frame passed as an argument
        timedelta (timedelta, optional): class timedelta as an dependency injection.
            Defaults to timedelta.

    Returns:
        str: a string representing the calculated timedelta in isoformat
    """
    calculated_date = date + timedelta(hours=delta)
    return calculated_date.isoformat()


def error_handling(e: Exception) -> Dict[str, str]:
    """function to handler and transform exceptions in Dict

    Args:
        e (Exception): The raised exception

    Returns:
        Dict[str, str]: exception name as key having their args as value
    """
    error_message = {
        'error_type': type(e).__name__,
        'error_message': str(e.args),
    }
    logger.error(str(error_message))
    return error_message


# %%
