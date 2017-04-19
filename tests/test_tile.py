import pytest
from pygeotile.tile import Tile


@pytest.fixture(scope='module')
def tms():
    return 67, 83


def test_from_google(tms):
    google_x, google_y = 67, 44

    tile = Tile.from_google(google_x=google_x, google_y=google_y, zoom=7)
    print(tile.tms)
    assert tile.tms == tms


def test_from_google_1():
    google_x, google_y = 1853, 1289
    tms_tasmania = 1853, 758

    tile = Tile.from_google(google_x=google_x, google_y=google_y, zoom=11)
    print(tile.tms)
    assert tile.tms == tms_tasmania


def test_from_tms(tms):
    tms_x, tms_y = tms

    tile = Tile.from_tms(tms_x=tms_x, tms_y=tms_y, zoom=7)

    assert tile.tms == tms
