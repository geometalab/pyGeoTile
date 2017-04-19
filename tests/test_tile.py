from pygeotile.tile import Tile


def test_from_google():
    google_x, google_y = 67, 44
    tms = 67, 83

    tile = Tile.from_google(google_x=google_x, google_y=google_y, zoom=7)
    print(tile.tms)
    assert tile.tms == tms


def test_from_google_1():
    google_x, google_y = 1853, 1289
    tms = 1853, 758

    tile = Tile.from_google(google_x=google_x, google_y=google_y, zoom=11)
    print(tile.tms)
    assert tile.tms == tms
