import math


class Meta:
    def __init__(self):
        self._tile_size = 256
        self._earth_radius = 6378137.0

    @property
    def earth_radius(self):
        return self._earth_radius

    @property
    def tile_size(self):
        return self._tile_size

    @property
    def origin_shift(self):
        return 2.0 * math.pi * self.earth_radius / 2.0

    @property
    def initial_resolution(self):
        return 2.0 * math.pi * self.earth_radius / float(self.tile_size)

    def resolution(self, zoom):
        return self.initial_resolution / (2 ** zoom)
