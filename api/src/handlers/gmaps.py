#%%
from typing import Dict

import googlemaps

from api.src.utils.logger import logger

# %%
gmaps = googlemaps.Client(key='AIzaSyAwDP4UE06S9XvS6M98mpWb8AN-VnOdhSs')


def get_geocode_from_postal(
    postal_code: str, gmaps: googlemaps.Client = gmaps
) -> tuple[float, ...]:
    """Convert a string into a coordinate

    Args:
        postal_code (str): A string representing, preferably, a postal or zip
        codes or any other valid address to geocode

        gmaps (googlemaps.Client, optional): The Client from googlemaps  as an
        dependency injection. Defaults to gmaps that represents an object of
        this class

    Raises:
        ValueError: Raises an error if the returning result is empty

    Returns:
        tuple[tuple(float, float), ...]: a collection of coordinates retrieved from google
            locations in forme of tuples of floating for each location as
            longitude as latitude
    """
    geocode_result = gmaps.geocode(postal_code)
    list_results = []
    if len(geocode_result) == 0:
        logger.error(
            "There's no known location for this zip or postal code {postal_code}"
        )
        raise ValueError(
            f"There's no known location for this zip or postal code {postal_code}"
        )
    else:
        for result in geocode_result:
            geometry = result.get('geometry')
            location = geometry.get('location')
            lon, lat = location.get('lng'), location.get('lat')
            list_results.append(tuple((lon, lat)))
            return tuple(list_results)


# %%
