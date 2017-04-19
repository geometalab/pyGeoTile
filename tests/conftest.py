import pytest

'''
Chicago, IL
LatLng: (41.85, -87.64999999999998)
Zoom level: 19
World Coordinate: (65.67111111111113, 95.17492654697409)
Pixel Coordinate: (34430575, 49899071)
Tile Coordinate: (134494, 194918)
'''


@pytest.fixture(scope="session", autouse=True)
def chicago_latitude_longitude():
    return 41.85, -87.65


@pytest.fixture(scope="session", autouse=True)
def chicago_zoom():
    return 19


@pytest.fixture(scope="session", autouse=True)
def chicago_pixel():
    return 34430575, 49899071


def chicago_pixel_bounds():
    return 34430464, 49899008, 34430720, 49899264


def chicago_meter_bounds():
    return -9757186.660602748, 5138479.226470973, -9757110.223574463, 5138555.663499258


def chicago_latitude_longitude_bounds():
    return 41.8496161693754, -87.65029907226562, 41.85012764855732, -87.64961242675781


@pytest.fixture(scope="session", autouse=True)
def chicago_google():
    return 134494, 194918


@pytest.fixture(scope="session", autouse=True)
def chicago_tms():
    return 134494, 329369


@pytest.fixture(scope="session", autouse=True)
def chicago_quad_tree():
    return '0302222310303211330'
