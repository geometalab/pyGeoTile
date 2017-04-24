import pytest
from pygeotile.meta import Meta


def test_meta():
    meta = Meta()

    assert meta.tile_size == 256
    assert meta.earth_radius == 6378137


