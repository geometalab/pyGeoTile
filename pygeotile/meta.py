import math

EARTH_RADIUS = 6378137.0
TILE_SIZE = 256
ORIGIN_SHIFT = 2.0 * math.pi * EARTH_RADIUS / 2.0
INITIAL_RESOLUTION = 2.0 * math.pi * EARTH_RADIUS / float(TILE_SIZE)


def resolution(zoom):
    return INITIAL_RESOLUTION / (2 ** zoom)
