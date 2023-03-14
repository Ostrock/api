from datetime import datetime as dt
from typing import Dict, TypedDict

from api.src.classes.Location import Location
from api.src.classes.SevenTimer import SevenTimer
from api.src.classes.WeatherTimeseries import WeatherTimeSeries
from api.src.handlers.gmaps import get_geocode_from_postal
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


def google_processor(input_str: str) -> WeatherInformationDict:
    """A processor to encapsulate all the process to get weather time series
    given a postal or zip code

    Args:
        input_str (str): A string representing, preferably, a postal or zip
        codes or any other valid address to geocode


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
    coordinates = get_geocode_from_postal(input_str)
    location = Location.get_location_from_google(coordinates)
    origin_information = SevenTimer.get(lon=location.lon, lat=location.lat)
    weather_forecasting = WeatherTimeSeries.get(
        lon=location.lon, lat=location.lat, now=now
    )
    weather_forecasting.calc_timeseries(origin_information.dataseries, now)

    return weather_forecasting.to_json()
