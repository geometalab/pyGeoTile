import pytest

from pygeotile.point import Point


@pytest.fixture(scope='module')
def coordinates():
    return 47.0, 8.0


def test_from_coordinates(coordinates):
    latitude, longitude = coordinates
    point = Point.from_coordinates(latitude=latitude, longitude=longitude)

    assert point.coordinates == coordinates


def test_from_meters(coordinates):
    meter_x = 890555.93
    meter_y = 5942074.07

    point = Point.from_meters(meter_x=meter_x, meter_y=meter_y)
    latitude, longitude = point.coordinates

    assert pytest.approx(latitude, 0.01) == coordinates[0]
    assert pytest.approx(longitude, 0.01) == coordinates[1]


def test_from_pixel(coordinates):
    meter_x = 890555.93
    meter_y = 5942074.07

def test_zoom_exception():
    point = Point()
    with pytest.raises(Exception) as exception:
        _ = point.zoom
    assert 'Zoom is not set!' in str(exception.value)
