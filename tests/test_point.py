import pytest

from pygeotile.point import Point


@pytest.fixture(scope='module')
def latitude_longitude():
    return 47.0, 8.0


def test_from_coordinates(latitude_longitude):
    latitude, longitude = latitude_longitude
    point = Point.from_latitude_longitude(latitude=latitude, longitude=longitude)

    assert point.latitude_longitude == latitude_longitude


def test_from_meters(chicago_latitude_longitude, chicago_meters):
    meter_x, meter_y = chicago_meters

    point = Point.from_meters(meter_x=meter_x, meter_y=meter_y)
    latitude, longitude = point.latitude_longitude

    assert pytest.approx(point.meters[0], 0.1) == meter_x
    assert pytest.approx(point.meters[1], 0.1) == meter_y

    assert pytest.approx(latitude, 0.1) == chicago_latitude_longitude[0]
    assert pytest.approx(longitude, 0.1) == chicago_latitude_longitude[1]


def test_from_pixel():
    point = Point.from_pixel(pixel_x=256, pixel_y=256, zoom=1)

    assert pytest.approx(point.meters[0], 0.2) == 0.0
    assert pytest.approx(point.meters[0], 0.2) == 0.0

    assert point.pixels[0] == 256
    assert point.pixels[1] == 256


def test_from_pixel_1():
    point = Point.from_pixel(pixel_x=0, pixel_y=512, zoom=1)
    origin_shift = 20037508.3428

    assert pytest.approx(point.meters[0], 0.2) == -origin_shift
    assert pytest.approx(point.meters[0], 0.2) == -origin_shift


def test_from_pixel_2():
    point = Point.from_pixel(pixel_x=512, pixel_y=512, zoom=1)
    origin_shift = 20037508.3428

    assert pytest.approx(point.meters[0], 0.2) == origin_shift
    assert pytest.approx(point.meters[0], 0.2) == -origin_shift


def test_from_pixel_3():
    point = Point.from_pixel(pixel_x=0, pixel_y=256, zoom=1)
    origin_shift = 20037508.3428

    assert pytest.approx(point.meters[0], 0.2) == 0
    assert pytest.approx(point.meters[0], 0.2) == -origin_shift


def test_from_pixel_chicago(chicago_latitude_longitude, chicago_pixel, chicago_zoom):
    latitude, longitude = chicago_latitude_longitude
    pixel_x, pixel_y = chicago_pixel

    point = Point.from_pixel(pixel_x=pixel_x, pixel_y=pixel_y, zoom=chicago_zoom)

    assert point.pixels == chicago_pixel
    assert pytest.approx(point.latitude_longitude[1], 0.2) == longitude
    assert pytest.approx(point.latitude_longitude[0], 0.2) == latitude
