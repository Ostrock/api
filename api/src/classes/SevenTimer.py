#%%
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime as dt
from typing import Dict

import requests

from api.src.utils.enums import baseurl
from api.src.utils.logger import logger


@dataclass
class SevenTimer:
    """A class used to represent the return from 7timer API

    Given a coordinate this class will validate the data and automatically
    instantiate the object

    Attributes
    ----------
    dataserires (list[Dict]): the data series list returned for a valid location
    response by the 7timer API

    Methods
    -------
    coordinate_type_validator(input_string: str) -> int
        Validate the type of a given coordinate

    transform_coordinate(cls, str_coordinate: str) -> float:
        classmethod to transform the valid coordinate into float

    coordinate_validator(cls, location: Dict[str, float]) -> bool
        Classmethod to check if the coordinate provided is valid

    get_location_from_string(cls, str_lon: str, str_lat: str) -> Location
        classmethod to construct the class from input string for lat and lon

    get_location_from_google(cls, google_results: tuple[tuple[float, ...]]) -> Location
        classmethod to construct the class from postal or zip codes and address

    to_json(self) -> Dict[str, float]:
        Method to return the instantiated object as a dict
    """

    dataseries: list[Dict]

    @classmethod
    def get(
        cls,
        lon: float,
        lat: float,
        requests: requests = requests,
        dt: dt = dt,
        url: str = baseurl,
    ) -> SevenTimer:
        """Function tht

        Args:
            lon (float): a float representing the intended Longitude
            lat (float): a float representing the intended Latitude
            requests (requests, optional): the module requests as an
                dependency injection. Defaults to requests
            dt (datetime, optional): the class datetime as an dependency
                injection. Defaults to datetime as dt.
            url (str, optional): the base url from external end point
                 Defaults to baseurl.
        """
        params: Dict[str, str] = {
            'lon': lon,
            'lat': lat,
            'unit': 'metric',
            'product': 'civil',
            'output': 'json',
        }
        i = params
        concat = f'lon={lon}&lat={lat}&unit=metric&product=civil&output=json'
        now = dt.utcnow()
        logger.info(f'initial time: {now}')
        logger.info(f'url: {baseurl+concat}')
        results = requests.get(url=baseurl, params=params)
        dataseries = results.json().get('dataseries')
        return cls(dataseries=dataseries)

    def to_json(self) -> Dict[str, any]:
        """Method to return the instantiated object as a dict

        Return the fields of a dataclass instance as a new dictionary mapping
        field names to field values.


        Returns:
            Dict[str, any]: Returns a dict to be converted to json with the
            attributes from class as keys and their value
        """
        return asdict(self)


# %%
