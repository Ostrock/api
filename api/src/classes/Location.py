#%%
# api consumption
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Dict

from api.src.utils.logger import logger


@dataclass
class Location:
    """A class used to represent an valid Coordinate in latitude and Longitude
    system

    Given a coordinate this class will validate the data and automatically
    instantiate the object

    Attributes
    ----------
    lon (float): a string representing the valid longitude
    lat (float): a string representing the valid latitude

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

    lon: float
    lat: float

    @classmethod
    def coordinate_type_validator(cls, input_string: str) -> int:
        """Validate the type of a given coordinate

        Given a latitude or longitude the function check the type.
        Considering that it can come in with or without the +/- signals, as an
        int, a float, having or not decimal numbers or having commas as
        decimal separator it's needed to validate the input type.

        The function uses regular expression to determine if the user provided
        a minimum valid coordinate that considering that the coordinate provided
        is in one of the following types:
        - Numbers with dot as decimal separator
        - Numbers with comma as decimal separator
        - Any other type of string

        Args:
            input_string (str): the provided coordinate

        Raises:
            ValueError: if the string is of the type None or has a len minor
            than one, meaning that is empty, the function raises ValueError

        Returns:
            int: an int from 0 to 2, inclusive, that will be interpreted by
            the class method transform_coordinate for one of the three types:
            - 1: Numbers with dot as decimal separator
            - 2: Numbers with comma as decimal separator
            - 0: Any other type of string
        """
        logger.info(f'{input_string}')
        if input_string is None or len(input_string) < 1:
            logger.error(f'Empty coordinate provided')
            raise ValueError('Empty coordinate provided')
        pattern_dot = re.compile(r'^(\+|-)?(\d{1,3}){1}\.?(\d+)?$')
        pattern_comma = re.compile(r'^(\+|-)?(\d{1,3}){1},?(\d+)?$')
        if pattern_dot.match(input_string):
            logger.info('coordinate provided in correct format')
            return 1
        elif pattern_comma.match(input_string):
            logger.warning(
                'coordinate is correct but has a comma as separator, prefer using dot instead'
            )
            return 2
        else:
            logger.info('coordinate provided in incorrect format')
            return 0

    @classmethod
    def transform_coordinate(cls, str_coordinate: str) -> float:
        """classmethod to transform the valid coordinate into float

        Args:
            str_coordinate (str): Given a valid coordinate, validated by
            class method coordinate_type_validator, if the return are 1 or 2
            this function will casting the string to float, replacing any comma
            that is present in type 2 to a dot providing a log warning alerting
            to the preferential use dot's instead commas

        Raises:
            ValueError: if the return from classmethod coordinate_type_validator
            is zero will raise a value error informing the user that this type
            can't be casted to float

        Returns:
            float: returns the casted string as a float
        """
        coordinate_type = cls.coordinate_type_validator(str_coordinate)
        if coordinate_type == 1:
            logger.info('valid coordinate')
            return float(str_coordinate)
        elif coordinate_type == 2:
            logger.info('coordinate provided with comma, prefer using dots')
            return float(str_coordinate.replace(',', '.'))
        else:
            logger.error(
                f"The coordinate couldn't be converted to float, check your input"
            )
            raise ValueError(
                "The coordinate couldn't be converted to float, check your input"
            )

    @classmethod
    def coordinate_validator(cls, location: Dict[str, float]) -> bool:
        """Classmethod to check if the coordinate provided is valid

        Given a dictionary with keys lon and lat this classmethod will validate
        if the coordinates passed to this function are into the floor ans
        ceiling boundaries of the latitude and longitude system.
        This method is to prevent calling  the external service if it can
        return an error.


        Args:
            location (Dict[str, float]): Receives a Dictionary with keys
            lon and lat from type float validated and converted from the original
            input string by classmethod transform_coordinate

        Raises:
            ValueError: If the coordinate passed is out of the boundaries of
            latitude and longitude system raises ValueError to avoid calling
            the external service

        Returns:
            bool: returns True if both latitude and longitude are valid
        """
        input_lat = location.get('lat')
        input_lon = location.get('lon')
        print(f'lat: {input_lat}')
        print(f'lat: {input_lon}')
        lat = True if input_lat >= -90.0 and input_lat <= 90.0 else False
        lon = True if input_lon >= -180.0 and input_lon <= 180.0 else False
        if lon and lat:
            return True
        else:
            logger.error(
                'The location provided is out of the boundaries of latitude and longitude system'
            )
            raise ValueError(
                'The location provided is out of the boundaries of latitude and longitude system'
            )

    @classmethod
    def get_location_from_string(cls, str_lon: str, str_lat: str) -> Location:
        """classmethod to construct the class from input string for lat and lon

        Given the parameters passed to the endpoint of the external service
        after the validation from classmethod coordinate_validator it will
        return a object of the class Location with attributes lon and lat

        Args:
            str_lon (str): a string representing the intended longitude
            str_lat (str): a string representing the intended latitude

        Raises:
            ValueError: Raises an ValueError if the object could'nt be
            instantiated correctly passing the parameters given to the external
            endpoint

        Returns:
            Location: Instantiated object of the class Location
        """
        logger.info(f'coordinates: {str_lon}, {str_lat}')
        try:
            location: Dict = {
                'lat': cls.transform_coordinate(str_lat),
                'lon': cls.transform_coordinate(str_lon),
            }
            valid_location = cls.coordinate_validator(location)
            if valid_location:
                return cls(**location)
        except Exception as e:
            logger.error(
                f'Some information are note correct, check if latitude {str_lat} and longitude {str_lon} are correct. Returning error: {str(e)}'
            )
            raise ValueError(
                f'Some information are note correct, check if latitude {str_lat} and longitude {str_lon} are correct. Returning error: {str(e)}'
            )

    @classmethod
    def get_location_from_google(
        cls, google_results: tuple[tuple[float, ...]]
    ) -> Location:
        """classmethod to construct the class from postal or zip codes and address

        Given a valid zip or postal code it is passed to googlemaps API and
        through the function get_geocode_from_postal and returns a tuple of
        valid coordinates for that information

        Args:
            google_results (tuple[tuple[float, ...]]): An coordinate provided
            by googlemaps api converted to tuple by the function
            get_geocode_from_postal

        Raises:
            ValueError: raises an ValueError if the googlemapsapi couldn't
            validate the zip or postal code, address or any other information
            passed to this function

        Returns:
            Location: Instantiated object of the class Location
        """
        try:
            location: Dict = {
                'lat': google_results[0][1],
                'lon': google_results[0][0],
            }
            valid_location = cls.coordinate_validator(location)
            if valid_location:
                logger.info('Valid location')
                return cls(**location)
        except Exception as e:
            logger.error(
                f'Some information are note correct, check if latitude {google_results[0][1]} and longitude {google_results[0][0]} are correct. Returning error: {str(e)}'
            )
            raise ValueError(
                f'Some information are note correct, check if latitude {google_results[0][1]} and longitude {google_results[0][0]} are correct. Returning error: {str(e)}'
            )

    def to_json(self) -> Dict[str, float]:
        """Method to return the instantiated object as a dict

        Return the fields of a dataclass instance as a new dictionary mapping
        field names to field values.


        Returns:
            Dict[str, float]: Returns a dict to be converted to json with the
            attributes from class as keys and their value
        """
        return asdict(self)


# %%
