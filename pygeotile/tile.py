import math
from functools import reduce

from .point import Point


class Tile:
    def __init__(self, tms_x=None, tms_y=None, zoom=None):
        self._tms_x = tms_x
        self._tms_y = tms_y
        self._zoom = zoom

    @classmethod
    def from_quad_tree(cls, quad_tree):
        zoom = len(str(quad_tree))
        offset = int(math.pow(2, zoom)) - 1
        tms_x, tmx_y = [reduce(lambda result, bit: (result << 1) | bit, bits, 0)
                        for bits in zip(*(reversed(divmod(digit, 2))
                                          for digit in (int(c) for c in str(quad_tree))))]
        return cls(tms_x=tms_x, tms_y=(offset - tmx_y))

    @classmethod
    def from_tms(cls, tms_x, tms_y, zoom):
        return cls(tms_x=tms_x, tms_y=tms_y, zoom=zoom)

    @classmethod
    def from_google(cls, google_x, google_y, zoom):
        return cls(tms_x=google_x, tms_y=(google_y % (2 ** zoom - 1)), zoom=zoom)

    @classmethod
    def for_pixels(cls, pixel_x, pixel_y):
        point = Point.from_pixel(pixel_x=pixel_x, pixel_y=pixel_y)
        tms_x = int(math.ceil(pixel_x / float(point.tile_size)) - 1)
        tms_y = int(math.ceil(pixel_y / float(point.tile_size)) - 1)
        return cls(tms_x=tms_x, tms_y=tms_y)

    @property
    def zoom(self):
        if not self._zoom:
            raise TypeError('Zoom is not set!')
        return self._zoom

    @property
    def tms(self):
        return self._tms_x, self._tms_y

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
