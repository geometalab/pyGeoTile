import math
from functools import reduce

from .point import Point
from .meta import Meta


class Tile(Meta):
    def __init__(self, tile_size=256, earth_radius=6378137, zoom=None):
        super().__init__(tile_size=tile_size, earth_radius=earth_radius)
        self._tms_x = None
        self._tms_y = None
        self._zoom = zoom

    @classmethod
    def from_quad_tree(cls, quad_tree):
        zoom = len(str(quad_tree))
        offset = int(math.pow(2, zoom)) - 1
        tms_x, tmx_y = [reduce(lambda result, bit: (result << 1) | bit, bits, 0)
                        for bits in zip(*(reversed(divmod(digit, 2))
                                          for digit in (int(c) for c in str(quad_tree))))]
        return cls.from_tms(tms_x=tms_x, tms_y=(offset - tmx_y), zoom=zoom)

    @classmethod
    def from_tms(cls, tms_x, tms_y, zoom):
        tile = cls(zoom=zoom)
        tile.tms = tms_x, tms_y
        return tile

    @classmethod
    def from_google(cls, google_x, google_y, zoom):
        tms_x, tms_y = (google_x, abs(google_y - (2 ** zoom - 1)))
        return cls.from_tms(tms_x=tms_x, tms_y=tms_y, zoom=zoom)

    @classmethod
    def for_pixels(cls, pixel_x, pixel_y, zoom):
        point = Point.from_pixel(pixel_x=pixel_x, pixel_y=pixel_y)
        tms_x = int(math.ceil(pixel_x / float(point.tile_size)) - 1)
        tms_y = int(math.ceil(pixel_y / float(point.tile_size)) - 1)
        return cls.from_tms(tms_x=tms_x, tms_y=tms_y, zoom=zoom)

    @property
    def zoom(self):
        if not self._zoom:
            raise TypeError('Zoom is not set!')
        return self._zoom

    @property
    def tms(self):
        return self._tms_x, self._tms_y

    @tms.setter
    def tms(self, value):
        if type(value) is tuple:
            tms_x, tms_y = value
            self._tms_x = tms_x
            self._tms_y = tms_y
        else:
            raise TypeError('Arguments of TMS needs to a tuple of X and Y!')

    @property
    def quad_tree(self):
        value = ''
        tms_x, tms_y = self.tms
        tms_y = (2 ** self.zoom - 1) - tms_y
        for i in range(self.zoom, 0, -1):
            digit = 0
            mask = 1 << (i - 1)
            if (tms_x & mask) != 0:
                digit += 1
            if (tms_y & mask) != 0:
                digit += 2
            value += str(digit)
        return value

    @property
    def google(self):
        tms_x, tms_y = self.tms
        return tms_x, (2 ** self.zoom - 1) - tms_y

    @property
    def bounds(self):
        tms_x, tms_y = self.tms
        pixel_x_min, pixel_y_min = tms_x * self.tile_size, tms_y * self.tile_size
        pixel_x_max, pixel_y_max = (tms_x + 1) * self.tile_size, (tms_y + 1) * self.tile_size

        point_min = Point.from_pixel(pixel_x=pixel_x_min, pixel_y=pixel_y_min, zoom=self.zoom)
        point_max = Point.from_pixel(pixel_x=pixel_x_max, pixel_y=pixel_y_max, zoom=self.zoom)
        return point_min, point_max
