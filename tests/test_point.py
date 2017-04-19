import pytest

from pygeotile.point import Point


@pytest.fixture(scope='module')
def latitude_longitude():
    return 47.0, 8.0


def test_from_coordinates(latitude_longitude):
    latitude, longitude = latitude_longitude
    point = Point.from_coordinates(latitude=latitude, longitude=longitude)

    assert point.latitude_longitude == latitude_longitude


def test_from_meters(latitude_longitude):
    meter_x = 890555.93
    meter_y = 5942074.07

    point = Point.from_meters(meter_x=meter_x, meter_y=meter_y)
    latitude, longitude = point.latitude_longitude

    assert pytest.approx(latitude, 0.01) == latitude_longitude[0]
    assert pytest.approx(longitude, 0.01) == latitude_longitude[1]


def test_from_pixel(chicago_latitude_longitude, chicago_pixel, chicago_zoom):
    latitude, longitude = chicago_latitude_longitude
    pixel_x, pixel_y = chicago_pixel

    point = Point.from_pixel(pixel_y=pixel_y, pixel_x=pixel_x, zoom=chicago_zoom)

    assert pytest.approx(point.latitude_longitude[0], 0.2) == latitude
    assert pytest.approx(point.latitude_longitude[1], 0.2) == longitude


