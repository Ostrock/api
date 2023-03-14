import pytest

from api.src.classes.SevenTimer import SevenTimer
from tests.mocks.requests import requests


def test_retrieve_data(fake_dataseries, fake_utcnow):
    expected = SevenTimer(fake_dataseries)
    result = SevenTimer.get(
        '46.8877366', '23.19351', requests, fake_utcnow, 'http'
    )
    assert expected == result


def test_instantiate_the_correct_a_seven_timer_object(
    fake_dataseries, fake_utcnow
):
    result = SevenTimer.get(
        '46.8877366', '23.19351', requests, fake_utcnow, 'http'
    )
    assert isinstance(result, SevenTimer)
