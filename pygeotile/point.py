import math
from .meta import Meta


class Point(Meta):
    def __init__(self, tile_size=256, earth_radius=6378137, zoom=None):
        super().__init__(tile_size=tile_size, earth_radius=earth_radius)
        self._latitude = None
        self._longitude = None
        self._zoom = zoom
        self._tile_size = tile_size
        self._earth_radius = earth_radius

    @classmethod
    def from_latitude_longitude(cls, latitude=0.0, longitude=0.0, zoom=None):
        point = cls(zoom=zoom)
        point.latitude_longitude = latitude, longitude
        return point

    @classmethod
    def from_pixel(cls, pixel_x=0, pixel_y=0, zoom=None):
        point = cls(zoom=zoom)
        meter_x = pixel_x * point.resolution - point.origin_shift
        meter_y = pixel_y * point.resolution - point.origin_shift
        return point.from_meters(meter_x=meter_x, meter_y=meter_y, zoom=zoom)

    @classmethod
    def from_meters(cls, meter_x=0.0, meter_y=0.0, zoom=None):
        point = cls(zoom=zoom)
        longitude = (meter_x / point.origin_shift) * 180.0
        latitude = (meter_y / point.origin_shift) * 180.0
        latitude = 180.0 / math.pi * (2 * math.atan(math.exp(latitude * math.pi / 180.0)) - math.pi / 2.0)
        return point.from_latitude_longitude(latitude=latitude, longitude=longitude, zoom=zoom)

    @property
    def latitude_longitude(self):
        return self._latitude, self._longitude

    @latitude_longitude.setter
    def latitude_longitude(self, value):
        if type(value) is tuple:
            latitude, longitude = value
            self._latitude = latitude
            self._longitude = longitude
        else:
            raise TypeError('Arguments of coordinates needs to a tuple of Latitude and Longitude!')

    @property
    def pixels(self):
        """Gets pixels of the EPSG:4326 pyramid by a specific zoom"""
        factor = 180 / self.initial_resolution / 2**self.zoom
        latitude, longitude = self.latitude_longitude
        pixel_x = (180 + latitude) / factor
        pixel_y = (90 + longitude) / factor
        return int(round(pixel_x)), int(round(pixel_y))

    @property
    def meters(self):
        """Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913"""
        latitude, longitude = self.latitude_longitude
        meter_x = longitude * self.origin_shift / 180.0

        #meter_y = math.log(math.atan(latitude * math.pi / 360 + math.pi / 4)) * self.origin_shift / math.pi
        meter_y = math.log(math.tan((90.0 + latitude) * math.pi / 360.0)) / (math.pi / 180.0)
        meter_y = meter_y * self.origin_shift / 180.0
        return meter_x, meter_y
