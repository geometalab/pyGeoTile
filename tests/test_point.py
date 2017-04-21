import pytest

from pygeotile.point import Point


@pytest.fixture(scope='module')
def latitude_longitude():
    return 47.0, 8.0


@pytest.fixture(scope='module')
def sign_meters():
    return 1, 1


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
    pixel_x, pixel_y = 256, 256
    point = Point.from_pixel(pixel_x=pixel_x, pixel_y=pixel_y, zoom=1)

    assert point.pixels == (pixel_x, pixel_y)
    assert pytest.approx(point.meters[0], 0.2) == 0.0
    assert pytest.approx(point.meters[0], 0.2) == 0.0


def test_from_pixel_1():
    pixel_x, pixel_y = 0, 512
    point = Point.from_pixel(pixel_x=pixel_x, pixel_y=pixel_y, zoom=1)

    assert point.pixels == (pixel_x, pixel_y)
    assert pytest.approx(point.meters[0], 0.2) == -point.origin_shift
    assert pytest.approx(point.meters[1], 0.2) == -point.origin_shift


def test_from_pixel_2():
    pixel_x, pixel_y = 512, 512
    point = Point.from_pixel(pixel_x=pixel_x, pixel_y=pixel_y, zoom=1)

    assert point.pixels == (pixel_x, pixel_y)
    assert pytest.approx(point.meters[0], 0.2) == point.origin_shift
    assert pytest.approx(point.meters[1], 0.2) == -point.origin_shift


def test_from_pixel_3():
    pixel_x, pixel_y = 0, 256
    point = Point.from_pixel(pixel_x=pixel_x, pixel_y=pixel_y, zoom=1)

    assert point.pixels == (pixel_x, pixel_y)
    assert pytest.approx(round(point.meters[1], 2), 0.2) == 0
    assert pytest.approx(point.meters[0], 0.2) == -point.origin_shift


def test_from_pixel_chicago(chicago_latitude_longitude, chicago_pixel, chicago_zoom):
    latitude, longitude = chicago_latitude_longitude
    pixel_x, pixel_y = chicago_pixel

    point = Point.from_pixel(pixel_x=pixel_x, pixel_y=pixel_y, zoom=chicago_zoom)

    assert point.pixels == chicago_pixel
    assert pytest.approx(point.latitude_longitude[1], 0.2) == longitude
    assert pytest.approx(point.latitude_longitude[0], 0.2) == latitude


def test_sign_1(sign_meters):
    pixel_x, pixel_y, zoom = 0.0, 0.0, 1
    point = Point(zoom=zoom)
    meter_x, meter_y = point._sign_meters(meters=sign_meters, pixels=(pixel_x, pixel_y))
    assert meter_x == -1
    assert meter_y == 1


def test_sign_2(sign_meters):
    pixel_x, pixel_y, zoom = 256.0, 256.0, 1
    point = Point(zoom=zoom)
    meter_x, meter_y = point._sign_meters(meters=sign_meters, pixels=(pixel_x, pixel_y))
    assert meter_x == 1
    assert meter_y == 1


def test_sign_3(sign_meters):
    pixel_x, pixel_y, zoom = 0.0, 512.0, 1
    point = Point(zoom=zoom)
    meter_x, meter_y = point._sign_meters(meters=sign_meters, pixels=(pixel_x, pixel_y))
    assert meter_x == -1
    assert meter_y == -1


def test_sign_4(sign_meters):
    pixel_x, pixel_y, zoom = 512.0, 512.0, 1
    point = Point(zoom=zoom)
    meter_x, meter_y = point._sign_meters(meters=sign_meters, pixels=(pixel_x, pixel_y))
    assert meter_x == 1
    assert meter_y == -1


def test_sign_5(sign_meters):
    pixel_x, pixel_y, zoom = 512.0, 0.0, 1
    point = Point(zoom=zoom)
    meter_x, meter_y = point._sign_meters(meters=sign_meters, pixels=(pixel_x, pixel_y))
    assert meter_x == 1
    assert meter_y == 1
