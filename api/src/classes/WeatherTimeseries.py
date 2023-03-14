#%%
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime as dt
from typing import Dict, Optional, TypedDict

from api.src.classes.WeatherInformation import WeatherInformation
from api.src.utils.enums import delta_time, time_limit
from api.src.utils.functions import date_calc
from api.src.utils.logger import logger

PartialWeatherInformation = TypedDict(
    'HeterogeneousDictionary',
    {
        'timestamp': str,
        'end_date': str,
        'lon': float,
        'lat': float,
        'dataseries': WeatherInformation,
    },
)


@dataclass
class WeatherTimeSeries:
    """A class used to represent a set of information retrieved from external
     endpoint

    Attributes
    ----------

    start_date: (str):a string representing a utc time in isoformat at the
        moment of processing

    end_date (string): a string representing a calculated utc time in isoformat

    lon (float): a float representation of a given Longitude

    lat (float): a float representation of a given Latitude

    timeseries (list[WeatherInformation]): an object that represents a time
    series and its encapsuled information

    Methods
    -------

    calc_timeseries(self, dataseries: list, now: str, time_limit: int = time_limit,
      date_calc: str = date_calc, ) -> WeatherTimeSeries:
        Update the attribute dataseries


    to_json(self) -> Dict[str, any]:
        Method to return the instantiated object as a dict
    """

    start_date: str
    end_date: str
    lon: float
    lat: float
    timeseries: Optional[list[WeatherInformation]] = None

    def calc_timeseries(
        self,
        dataseries: list,
        now: str,
        time_limit: int = time_limit,
        date_calc: str = date_calc,
    ) -> WeatherTimeSeries:
        """Update the attribute dataseries

        Given a received data series from external endpoint partially
        instantiated and then, updates this object with open_sky attribute

        Args:
            time_limit (int): an int representing a maximum of objects in data
            series calculated by rounding the quotient of delta_time by time_frame
            dataseries (list): _description_
            now (dt): _description_
            date_calc (dt, optional): _description_. Defaults to date_calc.

        Returns:
            WeatherTimeSeries: An instantiated object of the class WeatherTimeSeries
        """
        result = list()
        logger.debug(dataseries)
        for data in dataseries[:time_limit]:
            constructor = {
                'utc_timestamp': date_calc(now, data.get('timepoint')),
                'cloud_cover': data.get('cloudcover'),
                'temperature': data.get('temp2m'),
            }
            result.append(WeatherInformation.get_open_sky(constructor))
        self.timeseries = result
        for weather in self.timeseries:
            weather.solar_calc()
        return self

    def to_json(self) -> Dict[str, any]:
        """Method to return the instantiated object as a dict

        Return the fields of a dataclass instance as a new dictionary mapping
        field names to field values.


        Returns:
            Dict[str, any]: Returns a dict to be converted to json with the
            attributes from class as keys and their value
        """
        return asdict(self)

    @classmethod
    def get(
        cls,
        lon: float,
        lat: float,
        now: dt = dt.utcnow(),
        date_calc: str = date_calc,
        delta: int = delta_time,
    ) -> WeatherTimeSeries:
        """class Method to construct the class

        Given a latitude longitude coordinate, an timestamp this method will
        calculate the end date of the time series passing the lon and lat to
        class attributes not initializing the timeseries attribute.

        Args:
            lon (float): an float representing a valid longitude
            lat (float): an float representing a valid latitude
            now (datetime, optional): Object of class datetime in utc. Defaults
              to utc at the time of processing.
            date_calc (function, optional): Pass the function date_calc as an
                dependency injection. Defaults to date_calc.
            delta (int, optional): the maximum hours to be calculate restricted
            by 168 as it is the limit of the api. Defaults to 48.

        Returns:
            WeatherTimeSeries: A partially instantiated object of the class
            WeatherTimeSeries
        """
        constructor = {
            'start_date': now.isoformat(),
            'end_date': date_calc(now, delta),
            'lon': lon,
            'lat': lat,
        }

        return cls(**constructor)


# %%
