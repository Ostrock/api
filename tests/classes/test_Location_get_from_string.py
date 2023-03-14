import logging
from unittest.mock import patch

import pytest

from api.src.classes.Location import Location


@pytest.mark.xfail
def test_correct_coordinate(float_converter, indi):
    with patch('classes.Location.transform_location') as trans:
        trans.return_value = float_converter
        expected = Location(lon=10.156, lat=48.789)
        result = Location.get_location_from_string('10.156', '48.789')
        assert expected == result
