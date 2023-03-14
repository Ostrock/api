import logging
from unittest.mock import patch

import pytest

from api.src.classes.Location import Location


def test_coordinaten_correct():
    with patch(
        'api.src.classes.Location.Location.coordinate_type_validator'
    ) as type_validator:
        type_validator.return_value = 1
        expected = 10.156
        result = Location.transform_coordinate('10.156')
        assert expected == result


def test_transform_coordinate_correct_log_message(caplog):
    with patch(
        'classes.Location.Location.coordinate_type_validator'
    ) as type_validator:
        type_validator.return_value(1)
        with caplog.at_level(logging.INFO):
            Location.transform_coordinate('10.156')
    assert 'valid coordinate' in caplog.text


def test_coordinate_correcy_twith_comma():
    with patch(
        'classes.Location.Location.coordinate_type_validator'
    ) as type_validator:
        type_validator.return_value = 2
        expected = 10.156
        result = Location.transform_coordinate('10,156')
        assert expected == result


def test_transmform_coordinate_correct_with_comma_message_log(caplog):
    with patch(
        'classes.Location.Location.coordinate_type_validator'
    ) as type_validator:
        type_validator.return_value = 2
        with caplog.at_level(logging.INFO):
            Location.transform_coordinate('10,156')
    assert 'coordinate provided with comma, prefer using dots' in caplog.text


def test_transform_coordinate_incorrect_should_raise_ValueError_message():
    with patch(
        'classes.Location.Location.coordinate_type_validator'
    ) as type_validator:
        type_validator.return_value = 0
        with pytest.raises(ValueError) as e:
            Location.transform_coordinate('test')
            assert (
                str(e.value)
                == "The coordinate couldn't be converted to float, check your input"
            )


def test_transform_coordinate_incorrect_should_raise_ValueError():
    with patch(
        'classes.Location.Location.coordinate_type_validator'
    ) as type_validator:
        type_validator.return_value = 0
        with pytest.raises(ValueError) as e:
            Location.transform_coordinate('test')


def test_transform_coordinate_incorrect_message_log(caplog):
    with patch(
        'classes.Location.Location.transform_coordinate'
    ) as type_validator:
        with pytest.raises(ValueError) as e:
            with caplog.at_level(logging.INFO):
                Location.transform_coordinate('test')
    assert (
        "The coordinate couldn't be converted to float, check your input"
        in caplog.text
    )
