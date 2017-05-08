import math
import re
from functools import reduce
from collections import namedtuple

from .point import Point
from .meta import TILE_SIZE

BaseTile = namedtuple('BaseTile', 'tms_x tms_y zoom')


class Tile(BaseTile):
    """Immutable Tile class"""

    @classmethod
    def from_quad_tree(cls, quad_tree):
        """Creates a tile from a Microsoft QuadTree"""
        assert bool(re.match('^[0-3]*$', quad_tree)), 'QuadTree value can only consists of the digits 0, 1, 2 and 3.'
        zoom = len(str(quad_tree))
        offset = int(math.pow(2, zoom)) - 1
        google_x, google_y = [reduce(lambda result, bit: (result << 1) | bit, bits, 0)
                              for bits in zip(*(reversed(divmod(digit, 2))
                                                for digit in (int(c) for c in str(quad_tree))))]
        return cls(tms_x=google_x, tms_y=(offset - google_y), zoom=zoom)

    @classmethod
    def from_tms(cls, tms_x, tms_y, zoom):
        """Creates a tile from Tile Map Service (TMS) X Y and zoom"""
        max_tile = (2 ** zoom) - 1
        assert 0 <= tms_x <= max_tile, 'TMS X needs to be a value between 0 and (2^zoom) -1.'
        assert 0 <= tms_y <= max_tile, 'TMS Y needs to be a value between 0 and (2^zoom) -1.'
        return cls(tms_x=tms_x, tms_y=tms_y, zoom=zoom)

    @classmethod
    def from_google(cls, google_x, google_y, zoom):
        """Creates a tile from Google format X Y and zoom"""
        max_tile = (2 ** zoom) - 1
        assert 0 <= google_x <= max_tile, 'Google X needs to be a value between 0 and (2^zoom) -1.'
        assert 0 <= google_y <= max_tile, 'Google Y needs to be a value between 0 and (2^zoom) -1.'
        return cls(tms_x=google_x, tms_y=(2 ** zoom - 1) - google_y, zoom=zoom)

    @classmethod
    def for_point(cls, point, zoom):
        """Creates a tile for given point"""
        latitude, longitude = point.latitude_longitude
        return cls.for_latitude_longitude(latitude=latitude, longitude=longitude, zoom=zoom)

    @classmethod
    def for_pixels(cls, pixel_x, pixel_y, zoom):
        """Creates a tile from pixels X Y Z (zoom) in pyramid"""
        tms_x = int(math.ceil(pixel_x / float(TILE_SIZE)) - 1)
        tms_y = int(math.ceil(pixel_y / float(TILE_SIZE)) - 1)
        return cls(tms_x=tms_x, tms_y=(2 ** zoom - 1) - tms_y, zoom=zoom)

    @classmethod
    def for_meters(cls, meter_x, meter_y, zoom):
        """Creates a tile from X Y meters in Spherical Mercator EPSG:900913"""
        point = Point.from_meters(meter_x=meter_x, meter_y=meter_y)
        pixel_x, pixel_y = point.pixels(zoom=zoom)
        return cls.for_pixels(pixel_x=pixel_x, pixel_y=pixel_y, zoom=zoom)

    @classmethod
    def for_latitude_longitude(cls, latitude, longitude, zoom):
        """Creates a tile from lat/lon in WGS84"""
        point = Point.from_latitude_longitude(latitude=latitude, longitude=longitude)
        pixel_x, pixel_y = point.pixels(zoom=zoom)
        return cls.for_pixels(pixel_x=pixel_x, pixel_y=pixel_y, zoom=zoom)

    @property
    def tms(self):
        """Gets the tile in pyramid from Tile Map Service (TMS)"""
        return self.tms_x, self.tms_y

    @property
    def quad_tree(self):
        """Gets the tile in the Microsoft QuadTree format, converted from TMS"""
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
        """Gets the tile in the Google format, converted from TMS"""
        tms_x, tms_y = self.tms
        return tms_x, (2 ** self.zoom - 1) - tms_y

    @property
    def bounds(self):
        """Gets the bounds of a tile represented as the most west and south point and the most east and north point"""
        google_x, google_y = self.google
        pixel_x_west, pixel_y_north = google_x * TILE_SIZE, google_y * TILE_SIZE
        pixel_x_east, pixel_y_south = (google_x + 1) * TILE_SIZE, (google_y + 1) * TILE_SIZE

        point_min = Point.from_pixel(pixel_x=pixel_x_west, pixel_y=pixel_y_south, zoom=self.zoom)
        point_max = Point.from_pixel(pixel_x=pixel_x_east, pixel_y=pixel_y_north, zoom=self.zoom)
        return point_min, point_max


__all__ = ['Tile']
