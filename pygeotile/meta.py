import math


class Meta:
    def __init__(self, tile_size=256, earth_radius=6378137, zoom=None):
        self._zoom = zoom
        self._tile_size = tile_size
        self._earth_radius = earth_radius

    @property
    def zoom(self):
        if not self._zoom:
            raise TypeError('Zoom is not set!')
        return self._zoom

    @zoom.setter
    def zoom(self, zoom):
        self._zoom = zoom

    @property
    def earth_radius(self):
        return self._earth_radius

    @property
    def tile_size(self):
        return self._tile_size

    @property
    def origin_shift(self):
        return 2 * math.pi * self.earth_radius / 2.0

    @property
    def initial_resolution(self):
        return 2 * math.pi * self.earth_radius / self.tile_size

    @property
    def resolution(self):
        """Resolution (meters/pixel) for given zoom level (measured at Equator)"""
        return self.initial_resolution / (2 ** self.zoom)
