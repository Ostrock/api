import logging
from unittest.mock import patch

import pytest

from api.src.classes.Location import Location


def test_coordinate_validator_test_correct_coordinates():
    expected = True
    result = Location.coordinate_validator({'lon': 10.156, 'lat': 48.789})
    assert expected == result


def test_coordinate_validator_respect_lon_floor_limit():
    with pytest.raises(ValueError) as e:
        Location.coordinate_validator({'lon': -180.1, 'lat': 48.789})


def test_coordinate_validator_respect_lon_floor_limit_log_message(caplog):
    with pytest.raises(ValueError) as e:
        with caplog.at_level(logging.INFO):
            Location.coordinate_validator({'lon': -180.1, 'lat': 48.789})
    assert (
        'The location provided is out of the boundaries of latitude and longitude system'
        in caplog.text
    )


def test_coordinate_validator_respect_lon_floor_limit_error_message():
    with pytest.raises(ValueError) as e:
        Location.coordinate_validator({'lon': -180.1, 'lat': 48.789})
        assert (
            str(e.value)
            == 'The location provided is out of the boundaries of latitude and longitude system'
        )


def test_coordinate_validator_respect_lon_ceiling_limit():
    with pytest.raises(ValueError) as e:
        Location.coordinate_validator({'lon': 180.1, 'lat': 48.789})


def test_coordinate_validator_respect_lon_ceiling_limit_log_message(caplog):
    with pytest.raises(ValueError) as e:
        with caplog.at_level(logging.INFO):
            Location.coordinate_validator({'lon': 180.1, 'lat': 48.789})
    assert (
        'The location provided is out of the boundaries of latitude and longitude system'
        in caplog.text
    )


def test_coordinate_validator_respect_lon_ceilin_limit_error_message():
    with pytest.raises(ValueError) as e:
        Location.coordinate_validator({'lon': 180.00000001, 'lat': 48.789})
        assert (
            str(e.value)
            == 'The location provided is out of the boundaries of latitude and longitude system'
        )


def test_coordinate_validator_respect_lat_floor_limit():
    with pytest.raises(ValueError) as e:
        Location.coordinate_validator({'lon': 10.156, 'lat': -90.1})


def test_coordinate_validator_respect_lat_floor_limit_log_message(caplog):
    with pytest.raises(ValueError) as e:
        with caplog.at_level(logging.INFO):
            Location.coordinate_validator({'lon': -10.156, 'lat': -90.1})
    assert (
        'The location provided is out of the boundaries of latitude and longitude system'
        in caplog.text
    )


def test_coordinate_validator_respect_lat_floor_limit_error_message():
    with pytest.raises(ValueError) as e:
        Location.coordinate_validator({'lon': -10.156, 'lat': -90.1})
        assert (
            str(e.value)
            == 'The location provided is out of the boundaries of latitude and longitude system'
        )


def test_coordinate_validator_respect_lat_ceiling_limit():
    with pytest.raises(ValueError) as e:
        Location.coordinate_validator({'lon': 10.156, 'lat': 90.1})


def test_coordinate_validator_respect_lat_ceiling_limit_log_message(caplog):
    with pytest.raises(ValueError) as e:
        with caplog.at_level(logging.INFO):
            Location.coordinate_validator({'lon': 10.156, 'lat': 90.1})
    assert (
        'The location provided is out of the boundaries of latitude and longitude system'
        in caplog.text
    )


def test_coordinate_validator_respect_lat_ceilin_limit_error_message():
    with pytest.raises(ValueError) as e:
        Location.coordinate_validator({'lon': 180.00000001, 'lat': 90.1})
        assert (
            str(e.value)
            == 'The location provided is out of the boundaries of latitude and longitude system'
        )
