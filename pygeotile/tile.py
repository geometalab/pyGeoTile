import math
from functools import reduce

from .point import Point
from .meta import Meta


class Tile(Meta):
    def __init__(self, tile_size=256, earth_radius=6378137.0, zoom=None):
        super(Tile, self).__init__(tile_size=tile_size, earth_radius=earth_radius)
        self._tms_x = None
        self._tms_y = None
        self._zoom = zoom

    @classmethod
    def from_quad_tree(cls, quad_tree):
        """Creates a tile from a Microsoft QuadTree"""
        zoom = len(str(quad_tree))
        offset = int(math.pow(2, zoom)) - 1
        google_x, google_y = [reduce(lambda result, bit: (result << 1) | bit, bits, 0)
                              for bits in zip(*(reversed(divmod(digit, 2))
                                                for digit in (int(c) for c in str(quad_tree))))]
        return cls.from_tms(tms_x=google_x, tms_y=(offset - google_y), zoom=zoom)

    @classmethod
    def from_tms(cls, tms_x, tms_y, zoom):
        """Creates a tile from Tile Map Service (TMS) X Y and zoom"""
        tile = cls(zoom=zoom)
        tile.tms = tms_x, tms_y
        return tile

    @classmethod
    def from_google(cls, google_x, google_y, zoom):
        """Creates a tile from Google format X Y and zoom"""
        tms_x, tms_y = (google_x, (2 ** zoom - 1) - google_y)
        return cls.from_tms(tms_x=tms_x, tms_y=tms_y, zoom=zoom)

    @classmethod
    def for_point(cls, point, zoom=None):
        """Creates a tile for given point"""
        latitude, longitude = point.latitude_longitude
        if zoom is None:
            zoom = point.zoom
        return cls.for_latitude_longitude(latitude=latitude, longitude=longitude, zoom=zoom)

    @classmethod
    def for_pixels(cls, pixel_x, pixel_y, zoom):
        """Creates a tile from pixels X Y Z (zoom) in pyramid"""
        tile = cls(zoom=zoom)
        tms_x = int(math.ceil(pixel_x / float(tile.tile_size)) - 1)
        tms_y = int(math.ceil(pixel_y / float(tile.tile_size)) - 1)
        tile.tms = tms_x, (2 ** zoom - 1) - tms_y
        return tile

    @classmethod
    def for_meters(cls, meter_x, meter_y, zoom):
        """Creates a tile from X Y meters in Spherical Mercator EPSG:900913"""
        point = Point.from_meters(meter_x=meter_x, meter_y=meter_y, zoom=zoom)
        pixel_x, pixel_y = point.pixels
        return cls.for_pixels(pixel_x=pixel_x, pixel_y=pixel_y, zoom=zoom)

    @classmethod
    def for_latitude_longitude(cls, latitude, longitude, zoom):
        """Creates a tile from lat/lon in WGS84"""
        point = Point.from_latitude_longitude(latitude=latitude, longitude=longitude, zoom=zoom)
        pixel_x, pixel_y = point.pixels
        return cls.for_pixels(pixel_x=pixel_x, pixel_y=pixel_y, zoom=zoom)

    @property
    def tms(self):
        """Gets the tile in pyramid from Tile Map Service (TMS)"""
        return self._tms_x, self._tms_y

    @tms.setter
    def tms(self, value):
        """Sets the tile in pyramid from Tile Map Service (TMS)"""
        if type(value) is tuple:
            tms_x, tms_y = value
            self._tms_x = tms_x
            self._tms_y = tms_y
        else:
            raise TypeError('Arguments of TMS needs to a tuple of X and Y!')

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
        pixel_x_west, pixel_y_north = google_x * self.tile_size, google_y * self.tile_size
        pixel_x_east, pixel_y_south = (google_x + 1) * self.tile_size, (google_y + 1) * self.tile_size

        point_min = Point.from_pixel(pixel_x=pixel_x_west, pixel_y=pixel_y_south, zoom=self.zoom)
        point_max = Point.from_pixel(pixel_x=pixel_x_east, pixel_y=pixel_y_north, zoom=self.zoom)
        return point_min, point_max
