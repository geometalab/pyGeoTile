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


def test_from_pixel():
    latitude, longitude = 41.85, -87.65
    pixel_x, pixel_y = (34430575, 49899071)

    point = Point.from_pixel(pixel_y=pixel_y, pixel_x=pixel_x, zoom=19)
    print(point.latitude_longitude)
    print(point.pixels)
    print(point.meters)

    assert pytest.approx(point.latitude_longitude[0], 0.2) == latitude
    assert pytest.approx(point.latitude_longitude[1], 0.2) == longitude


def test_zoom_exception():
    point = Point()
    with pytest.raises(Exception) as exception:
        _ = point.zoom
    assert 'Zoom is not set!' in str(exception.value)


'''
Chicago, IL
LatLng: (41.85, -87.64999999999998)
Zoom level: 19
World Coordinate: (65.67111111111113, 95.17492654697409)
Pixel Coordinate: (34430575, 49899071)
Tile Coordinate: (134494, 194918)
'''

'''
mx: 4658720.69
my: -24790661.63

LatLng: 41.85, -87.65
'''
