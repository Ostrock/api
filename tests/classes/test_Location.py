import logging
from unittest.mock import patch

import pytest

from api.src.classes.Location import Location

logger = logging.getLogger(__name__)


def test_coordinate_type_validator_none():
    with pytest.raises(ValueError) as e:
        Location.coordinate_type_validator(None)
        assert str(e.value) == 'Empty coordinate provided'


def test_coordinate_type_validator_empty_string():
    with pytest.raises(ValueError) as e:
        Location.coordinate_type_validator('')
        assert str(e.value) == 'Empty coordinate provided'


def test_coordinate_type_validator_coordinate_is_correct():
    expected = 1
    result = Location.coordinate_type_validator('45.456')
    assert expected == result


def test_coordinate_type_validator_coordinate_has_plus_signal_correct():
    expected = 1
    result = Location.coordinate_type_validator('+45.456')
    assert expected == result


def test_coordinate_type_validator_coordinate_has_minus_signal_correct():
    expected = 1
    result = Location.coordinate_type_validator('-45.456')
    assert expected == result


def test_coordinate_type_validator_coordinate_without_decimals():
    expected = 1
    result = Location.coordinate_type_validator('0')
    assert expected == result


def test_coordinate_type_validator_coordinate_whem_return_0_log_error_message(
    caplog,
):
    with caplog.at_level(logging.INFO):
        Location.coordinate_type_validator('-45.12345678')
    assert 'coordinate provided in correct format' in caplog.text


def test_coordinate_type_validator_coordinate_comma_plus_signal_correct():
    expected = 2
    result = Location.coordinate_type_validator('+45,456')
    assert expected == result


def test_coordinate_type_validator_coordinate_has_comma_minus_signal_correct():
    expected = 2
    result = Location.coordinate_type_validator('-45,56')
    assert expected == result


def test_coordinate_type_validator_coordinate_whem_return_0_log_error_message(
    caplog,
):
    with caplog.at_level(logging.INFO):
        Location.coordinate_type_validator('-45.12345678')
    assert 'coordinate provided in correct format' in caplog.text


# def test_coordinate_type_validator_coordinate_more_than_8_decimal_places():
# com oito decimais a medida alcança os milimetros, mas o retorno de uma coor
# denada com o Google ultrapassa esse valor, o que poderia invalidar um resulta
# do correto, sendo assim, foi retirada a validação dos campos decimais
#    expected = 0
#    result = Location.coordinate_type_validator("-45.123456789")
#    assert expected == result


def test_coordinate_type_validator_coordinate_whem_return_zero_log_error_message(
    caplog,
):
    """
    Não estava passando pois seguia a mesma lógica da exceção acima, o número correto
    com mais de oito caracteres deveria, até então ser considerado invalido.
    """
    with caplog.at_level(logging.INFO):
        Location.coordinate_type_validator('-ondetwothrew')
        assert 'coordinate provided in incorrect format' in caplog.text
