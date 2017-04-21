import pytest
from pygeotile.tile import Tile
from pygeotile.tile import Point


@pytest.fixture(scope='module')
def tms():
    return 67, 83


@pytest.fixture(scope='module')
def google():
    return 67, 44


@pytest.fixture(scope='module')
def quad_tree():
    return '1202211'


@pytest.fixture(scope='module')
def zoom():
    return 7


def test_from_google(tms, google, zoom):
    google_x, google_y = google

    tile = Tile.from_google(google_x=google_x, google_y=google_y, zoom=zoom)
    print(tile.tms)
    assert tile.tms == tms


def test_from_google_1():
    google_x, google_y = 1853, 1289
    tms_tasmania = 1853, 758

    tile = Tile.from_google(google_x=google_x, google_y=google_y, zoom=11)
    print(tile.tms)
    assert tile.tms == tms_tasmania


def test_from_tms(tms, zoom):
    tms_x, tms_y = tms

    tile = Tile.from_tms(tms_x=tms_x, tms_y=tms_y, zoom=zoom)

    assert tile.tms == tms


def test_from_quad_tree(tms, quad_tree, zoom):
    tile = Tile.from_quad_tree(quad_tree=quad_tree)

    assert tile.tms == tms
    assert tile.zoom == zoom


def test_cross_check(tms, google, quad_tree, zoom):
    tile = Tile.from_quad_tree(quad_tree=quad_tree)

    assert tile.tms == tms
    assert tile.zoom == zoom
    assert tile.google == google


def test_for_pixel(chicago_pixel, chicago_zoom, chicago_tms):
    pixel_x, pixel_y = chicago_pixel

    tile = Tile.for_pixels(pixel_x=pixel_x, pixel_y=pixel_y, zoom=chicago_zoom)

    assert tile.tms == chicago_tms


def test_for_meters(chicago_pixel, chicago_zoom, chicago_tms):
    pixel_x, pixel_y = chicago_pixel
    point = Point.from_pixel(pixel_x=pixel_x, pixel_y=pixel_y, zoom=chicago_zoom)
    meter_x, meter_y = point.meters

    tile = Tile.for_meters(meter_x=meter_x, meter_y=meter_y, zoom=chicago_zoom)

    assert tile.tms == chicago_tms


def test_pixel_bounds(chicago_quad_tree, chicago_pixel_bounds):
    tile = Tile.from_quad_tree(chicago_quad_tree)

    point_min, point_max = tile.bounds

    assert chicago_pixel_bounds[0] == point_min.pixels
    assert chicago_pixel_bounds[1] == point_max.pixels
