#%%
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, TypedDict

from api.src.utils.enums import solar_reference
from api.src.utils.logger import logger

PartialWeatherInformation = TypedDict(
    'HeterogeneousDictionary',
    {'timestamp': str, 'cloud_cover': int, 'temperature': int},
)


@dataclass
class WeatherInformation:
    """A class used to represent a set of information retrieved from external
     endpoint

    Given a coordinate this class pass the information gather from the external
    endpoint to represent each data series

    Attributes
    ----------

    utc_timestamp (str):a string representing a calculated utc time in isoformat

    cloud_cover (int): an int representing an abstraction of average cloud cover

    temperature (int): an int representing the celsius temperature

    open_sky (float): an float representing the average area retrieved that
        are not covered by clouds

    Methods
    -------

    solar_calc(self, solar: Dict[int, float] = solar_reference) -> WeatherInformation:
        Method to update the Attribute open.sky a float representing the
        average solar radiation in the area returned

    get_open_sky(cls, data: PartialWeatherInformation) -> WeatherInformation:
        classmethod to construct the class given a heterogenous dictionary

    """

    utc_timestamp: str
    cloud_cover: int
    temperature: int
    open_sky: float = field(init=False)

    def solar_calc(
        self, solar: Dict[int, float] = solar_reference
    ) -> WeatherInformation:
        """Method to update the Attribute open.sky a float representing the
        average solar radiation in the area returned

        Given an area the SevenTimer will receive the parameter cloud cover for
        the area of the 10 km²  with passed location in the middle of this area.

        7timer's wiki has a table references the number obtained and
        an estimate of the area covered by clouds.

        As the minimal and maximum cloud_cover are shared between the references
        a calculation is made to obtain the average of the opposite data given.

        If this data represents the coberture of the clouds so, the opposite is area
        receiving direct solar radiation represented in the enum solar_reference
        dict

        Args:
            solar (Dict[int, float], optional): An dictionary to make obtain the
            reference calculated. Defaults to utils.enums.solar_reference.

        Returns:
            WeatherInformation: An updated object of the class WeatherInformation
        """
        self.open_sky = solar.get(self.cloud_cover)
        return self

    @classmethod
    def get_open_sky(
        cls, data: PartialWeatherInformation
    ) -> WeatherInformation:
        """classmethod to construct the class given a heterogenous dictionary

        Given an PartialWeatherInformation dict, that is a heterogenous dict,
        this classmethod will converting the cloud_cover to estimated an average solar
        radiation in a given area

        Args:
            data (PartialWeatherInformation): receives an heterogeneous dict of
            representing partially initialized object WeatherTimeseries to update
            the attribute open_sky

        Returns:
            WeatherInformation: Instantiated object of the class WeatherInformation
        """
        return cls(**data)
