import math
import pytest

from pygeotile.point import Point

earth_radius = 6378137.0
origin_shift = 2.0 * math.pi * earth_radius / 2.0


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

    assert point.meters == pytest.approx(chicago_meters, abs=0.1)
    assert point.latitude_longitude == pytest.approx(chicago_latitude_longitude, abs=0.1)


def test_from_pixel_chicago(chicago_latitude_longitude, chicago_pixel, chicago_zoom):
    pixel_x, pixel_y = chicago_pixel

    point = Point.from_pixel(pixel_x=pixel_x, pixel_y=pixel_y, zoom=chicago_zoom)

    assert point.pixels(zoom=chicago_zoom) == chicago_pixel
    assert point.latitude_longitude == pytest.approx(chicago_latitude_longitude, abs=0.2)


@pytest.mark.parametrize("pixel_x, pixel_y,zoom, expected", [
    (0, 0, 1, (-origin_shift, origin_shift)),
    (256, 0, 1, (0, origin_shift)),
    (512, 0, 1, (origin_shift, origin_shift)),
    (0, 256, 1, (-origin_shift, 0)),
    (256, 256, 1, (0, 0)),
    (512, 256, 1, (origin_shift, 0)),
    (0, 512, 1, (-origin_shift, -origin_shift)),
    (256, 512, 1, (0, -origin_shift)),
    (512, 512, 1, (origin_shift, -origin_shift)),
])
def test_pixels_to_meters(pixel_x, pixel_y, zoom, expected):
    point = Point.from_pixel(pixel_x=pixel_x, pixel_y=pixel_y, zoom=zoom)

    assert point.meters == pytest.approx(expected, abs=0.1)
    assert point.pixels(zoom=zoom) == (pixel_x, pixel_y)


@pytest.mark.parametrize("pixel_x, pixel_y,zoom, expected", [
    (0, 0, 1, (85.05, -180.0)),
    (256, 0, 1, (85.05, 0)),
    (512, 0, 1, (85.05, 180.0)),
    (0, 256, 1, (0, -180.0)),
    (256, 256, 1, (0.0, 0.0)),
    (512, 256, 1, (0.0, 180.0)),
    (0, 512, 1, (-85.05, -180.0)),
    (256, 512, 1, (-85.05, 0.0)),
    (512, 512, 1, (-85.05, 180.0)),
])
def test_pixels_to_latitude_longitude(pixel_x, pixel_y, zoom, expected):
    point = Point.from_pixel(pixel_x=pixel_x, pixel_y=pixel_y, zoom=zoom)

    assert point.latitude_longitude == pytest.approx(expected, abs=0.1)
    assert point.pixels(zoom=zoom) == (pixel_x, pixel_y)


@pytest.mark.parametrize("meter_x, meter_y, expected", [
    (-origin_shift, origin_shift, (85.05, -180.0)),
    (0, origin_shift, (85.05, 0)),
    (origin_shift, origin_shift, (85.05, 180.0)),
    (-origin_shift, 0, (0, -180.0)),
    (0, 0, (0.0, 0.0)),
    (origin_shift, 0, (0.0, 180.0)),
    (-origin_shift, -origin_shift, (-85.05, -180.0)),
    (0, -origin_shift, (-85.05, 0.0)),
    (origin_shift, -origin_shift, (-85.05, 180.0)),
])
def test_meters_to_pixels(meter_x, meter_y, expected):
    point = Point.from_meters(meter_x=meter_x, meter_y=meter_y)

    assert point.latitude_longitude == pytest.approx(expected, abs=0.1)
    assert point.meters == pytest.approx((meter_x, meter_y), abs=0.1)


def test_latitude_longitude_setter():
    point = Point()
    latitude_longitude = (48.0, 8.0)
    point.latitude_longitude = latitude_longitude
    assert point.latitude_longitude == latitude_longitude


def test_latitude_longitude_setter_exception():
    point = Point()
    with pytest.raises(Exception) as exception:
        point.latitude_longitude = 10
    assert 'Arguments of coordinates needs to a tuple of Latitude and Longitude!' in str(exception.value)
