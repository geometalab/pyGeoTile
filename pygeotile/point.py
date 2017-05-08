import math
from collections import namedtuple
from .meta import resolution, ORIGIN_SHIFT, TILE_SIZE

BasePoint = namedtuple('BasePoint', 'latitude longitude')


class Point(BasePoint):
    """Immutable Point class"""

    @classmethod
    def from_latitude_longitude(cls, latitude=0.0, longitude=0.0):
        """Creates a point from lat/lon in WGS84"""
        assert -180.0 <= longitude <= 180.0, 'Longitude needs to be a value between -180.0 and 180.0.'
        assert -90.0 <= latitude <= 90.0, 'Latitude needs to be a value between -90.0 and 90.0.'
        return cls(latitude=latitude, longitude=longitude)

    @classmethod
    def from_pixel(cls, pixel_x=0, pixel_y=0, zoom=None):
        """Creates a point from pixels X Y Z (zoom) in pyramid"""
        max_pixel = (2 ** zoom) * TILE_SIZE
        assert 0 <= pixel_x <= max_pixel, 'Point X needs to be a value between 0 and (2^zoom) * 256.'
        assert 0 <= pixel_y <= max_pixel, 'Point Y needs to be a value between 0 and (2^zoom) * 256.'
        meter_x = pixel_x * resolution(zoom) - ORIGIN_SHIFT
        meter_y = pixel_y * resolution(zoom) - ORIGIN_SHIFT
        meter_x, meter_y = cls._sign_meters(meters=(meter_x, meter_y), pixels=(pixel_x, pixel_y), zoom=zoom)
        return cls.from_meters(meter_x=meter_x, meter_y=meter_y)

    @classmethod
    def from_meters(cls, meter_x=0.0, meter_y=0.0):
        """Creates a point from X Y Z (zoom) meters in Spherical Mercator EPSG:900913"""
        assert -ORIGIN_SHIFT <= meter_x <= ORIGIN_SHIFT, \
            'Meter X needs to be a value between -{0} and {0}.'.format(ORIGIN_SHIFT)
        assert -ORIGIN_SHIFT <= meter_y <= ORIGIN_SHIFT, \
            'Meter Y needs to be a value between -{0} and {0}.'.format(ORIGIN_SHIFT)
        longitude = (meter_x / ORIGIN_SHIFT) * 180.0
        latitude = (meter_y / ORIGIN_SHIFT) * 180.0
        latitude = 180.0 / math.pi * (2 * math.atan(math.exp(latitude * math.pi / 180.0)) - math.pi / 2.0)
        return cls(latitude=latitude, longitude=longitude)

    @property
    def latitude_longitude(self):
        """Gets lat/lon in WGS84"""
        return self.latitude, self.longitude

    def pixels(self, zoom=None):
        """Gets pixels of the EPSG:4326 pyramid by a specific zoom, converted from lat/lon in WGS84"""
        meter_x, meter_y = self.meters
        pixel_x = (meter_x + ORIGIN_SHIFT) / resolution(zoom=zoom)
        pixel_y = (meter_y - ORIGIN_SHIFT) / resolution(zoom=zoom)
        return abs(round(pixel_x)), abs(round(pixel_y))

    @property
    def meters(self):
        """Gets the XY meters in Spherical Mercator EPSG:900913, converted from lat/lon in WGS84"""
        latitude, longitude = self.latitude_longitude
        meter_x = longitude * ORIGIN_SHIFT / 180.0
        meter_y = math.log(math.tan((90.0 + latitude) * math.pi / 360.0)) / (math.pi / 180.0)
        meter_y = meter_y * ORIGIN_SHIFT / 180.0
        return meter_x, meter_y

    @staticmethod
    def _sign_meters(meters, pixels, zoom):
        half_size = int((TILE_SIZE * 2 ** zoom) / 2)
        pixel_x, pixel_y = pixels
        meter_x, meter_y = meters
        meter_x, meter_y = abs(meter_x), abs(meter_y)
        if pixel_x < half_size:
            meter_x *= -1
        if pixel_y > half_size:
            meter_y *= -1
        return meter_x, meter_y


__all__ = ['Point']
