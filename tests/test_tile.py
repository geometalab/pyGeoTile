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
    assert tile.tms == tms


def test_from_google_tasmania():
    google_x, google_y = 1853, 1289
    tms_tasmania = 1853, 758

    tile = Tile.from_google(google_x=google_x, google_y=google_y, zoom=11)
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
    assert tile.quad_tree == quad_tree


def test_for_pixel_chicago(chicago_pixel, chicago_zoom, chicago_tms):
    pixel_x, pixel_y = chicago_pixel

    tile = Tile.for_pixels(pixel_x=pixel_x, pixel_y=pixel_y, zoom=chicago_zoom)

    assert tile.tms == chicago_tms


def test_for_meters_chicago(chicago_pixel, chicago_zoom, chicago_tms):
    pixel_x, pixel_y = chicago_pixel
    point = Point.from_pixel(pixel_x=pixel_x, pixel_y=pixel_y, zoom=chicago_zoom)
    meter_x, meter_y = point.meters

    tile = Tile.for_meters(meter_x=meter_x, meter_y=meter_y, zoom=chicago_zoom)

    assert tile.tms == chicago_tms


def test_pixel_bounds_chicago(chicago_quad_tree, chicago_pixel_bounds):
    tile = Tile.from_quad_tree(chicago_quad_tree)

    point_min, point_max = tile.bounds

    assert chicago_pixel_bounds[0] == point_min.pixels(zoom=tile.zoom)
    assert chicago_pixel_bounds[1] == point_max.pixels(zoom=tile.zoom)


@pytest.mark.parametrize("tms_x, tms_y, zoom, expected_min, expected_max", [
    (0, 1, 1, (0.0, -180.0), (85.05, 0.0)),
    (1, 1, 1, (0.0, 0.0), (85.05, 180.0)),
    (0, 0, 1, (-85.05, -180.0), (0.0, 0.0)),
    (1, 0, 1, (-85.05, 0.0), (0.0, 180.0)),
])
def test_tile_bounds(tms_x, tms_y, zoom, expected_min, expected_max):
    tile = Tile.from_tms(tms_x=tms_x, tms_y=tms_y, zoom=zoom)
    point_min, point_max = tile.bounds

    assert point_min.latitude_longitude == pytest.approx(expected_min, abs=0.1)
    assert point_max.latitude_longitude == pytest.approx(expected_max, abs=0.1)


def test_for_latitude_longitude(chicago_latitude_longitude, chicago_zoom, chicago_tms):
    latitude, longitude = chicago_latitude_longitude
    tile = Tile.for_latitude_longitude(latitude=latitude, longitude=longitude, zoom=chicago_zoom)

    assert tile.tms == chicago_tms


def test_for_point(chicago_latitude_longitude, chicago_zoom, chicago_tms):
    latitude, longitude = chicago_latitude_longitude
    point = Point.from_latitude_longitude(latitude=latitude, longitude=longitude)
    tile = Tile.for_point(point=point, zoom=chicago_zoom)

    assert tile.tms == chicago_tms
    assert tile.zoom == chicago_zoom


assert_tms = [(-1, 2), (-5, 2), (4, 2), (10, 2)]
no_assert_tms = [(0, 2), (1, 2), (2, 2), (3, 2)]


@pytest.mark.parametrize("tms_x, zoom", assert_tms)
def test_assert_tms_x(tms_x, zoom):
    tms_y = 0

    with pytest.raises(AssertionError) as assertion_info:
        _ = Tile.from_tms(tms_x=tms_x, tms_y=tms_y, zoom=zoom)

    assert 'TMS X needs to be a value between 0 and (2^zoom) -1.' in str(assertion_info.value)


@pytest.mark.parametrize("tms_x, zoom", no_assert_tms)
def test_no_assert_tms_x(tms_x, zoom):
    tms_y = 0
    _ = Tile.from_tms(tms_x=tms_x, tms_y=tms_y, zoom=zoom)
    assert "No assertion raise :)"


@pytest.mark.parametrize("tms_y, zoom", assert_tms)
def test_assert_tms_y(tms_y, zoom):
    tms_x = 0

    with pytest.raises(AssertionError) as assertion_info:
        _ = Tile.from_tms(tms_x=tms_x, tms_y=tms_y, zoom=zoom)

    assert 'TMS Y needs to be a value between 0 and (2^zoom) -1.' in str(assertion_info.value)


@pytest.mark.parametrize("tms_y, zoom", no_assert_tms)
def test_no_assert_tms_y(tms_y, zoom):
    tms_x = 0
    _ = Tile.from_tms(tms_x=tms_x, tms_y=tms_y, zoom=zoom)
    assert "No assertion raise :)"


@pytest.mark.parametrize("google_x, zoom", assert_tms)
def test_assert_google_x(google_x, zoom):
    google_y = 0

    with pytest.raises(AssertionError) as assertion_info:
        _ = Tile.from_google(google_x=google_x, google_y=google_y, zoom=zoom)

    assert 'Google X needs to be a value between 0 and (2^zoom) -1.' in str(assertion_info.value)


@pytest.mark.parametrize("google_x, zoom", no_assert_tms)
def test_no_assert_google_x(google_x, zoom):
    google_y = 0
    _ = Tile.from_google(google_x=google_x, google_y=google_y, zoom=zoom)
    assert "No assertion raise :)"


@pytest.mark.parametrize("google_y, zoom", assert_tms)
def test_assert_google_y(google_y, zoom):
    google_x = 0

    with pytest.raises(AssertionError) as assertion_info:
        _ = Tile.from_google(google_x=google_x, google_y=google_y, zoom=zoom)

    assert 'Google Y needs to be a value between 0 and (2^zoom) -1.' in str(assertion_info.value)


@pytest.mark.parametrize("google_y, zoom", no_assert_tms)
def test_no_assert_google_y(google_y, zoom):
    google_x = 0
    _ = Tile.from_google(google_x=google_x, google_y=google_y, zoom=zoom)
    assert "No assertion raise :)"


@pytest.mark.parametrize("quad_tree", ['-1', '1235', 'aba', '9988'])
def test_assert_quad_tree(quad_tree):
    with pytest.raises(AssertionError) as assertion_info:
        _ = Tile.from_quad_tree(quad_tree=quad_tree)

    assert 'QuadTree value can only consists of the digits 0, 1, 2 and 3.' in str(assertion_info.value)


@pytest.mark.parametrize("quad_tree", ['1', '0123', '1231230', '00012'])
def test_no_assert_quad_tree(quad_tree):
    _ = Tile.from_quad_tree(quad_tree=quad_tree)
    assert "No assertion raise :)"
