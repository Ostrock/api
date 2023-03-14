#%%
from datetime import datetime as dt
from typing import Dict, TypedDict

from api.src.classes.Location import Location
from api.src.classes.SevenTimer import SevenTimer
from api.src.classes.WeatherTimeseries import WeatherTimeSeries
from api.src.utils.enums import time_limit
from api.src.utils.logger import logger

WeatherInformationDict = TypedDict(
    'HeterogeneousDictionary',
    {
        'timestamp': str,
        'cloud_cover': int,
        'temperature': int,
        'open_sky': float,
    },
)

WeatherTimeSeriesDict = TypedDict(
    'HeterogeneousDictionary',
    {
        'timestamp': str,
        'end_date': str,
        'lon': float,
        'lat': float,
        'dataseries': list[WeatherInformationDict],
    },
)


def string_processor(lon: str, lat: str) -> WeatherTimeSeriesDict:
    """A processor to encapsulate all the process to get weather time series
    for a given coordinate

    Args:
        lon (str): A string representation of a intended longitude
        lat (str): A string representation of a intended latitude

    Returns:
        WeatherInformationDict: A dictionary containing the following pair of
        key values:
            - "timestamp": str,
            - "end_date": str,
            - "lon": float,
            - "lat": float,
            - "dataseries": [
                             "timestamp": str,
                             "cloud_cover": int,
                             "temperature": int,
                             "open_sky": float
            ]
    """
    now = dt.utcnow()
    location = Location.get_location_from_string(lon, lat)
    origin_information = SevenTimer.get(lon=location.lon, lat=location.lat)
    weather_forecasting = WeatherTimeSeries.get(
        lon=location.lon, lat=location.lat, now=now
    )
    weather_forecasting.calc_timeseries(origin_information.dataseries, now)

    return weather_forecasting.to_json()


# %%
