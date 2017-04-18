import math
from .meta import Meta


class Point(Meta):
    def __init__(self, latitude=0.0, longitude=0.0, zoom=None):
        Meta.__init__(self, zoom=zoom)
        self._latitude = latitude
        self._longitude = longitude

    @classmethod
    def from_coordinates(cls, latitude=0.0, longitude=0.0):
        return cls(latitude=latitude, longitude=longitude)

    @classmethod
    def from_pixel(cls, pixel_x=0, pixel_y=0, zoom=0):
        return cls(latitude=latitude, longitude=longitude, zoom=zoom)

    @property
    def coordinates(self):
        return self._latitude, self._longitude

    @property
    def pixels(self):
        """Gets pixels of the EPSG:4326 pyramid by a specific zoom"""
        resolution = self.resolution()
        pixel_x = (180 + self._latitude) / resolution
        pixel_y = (90 + self._longitude) / resolution
        return pixel_x, pixel_y

    def _pixels_to_lat_lon(self, pixel_x=0, pixel_y=0, zoom=0):
        pass

    @property
    def meters(self):
        """Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913"""
        latitude, longitude = self.coordinates
        meter_x = longitude * self.origin_shift / 180.0
        meter_y = math.log(math.tan((90 + longitude) * math.pi / 360.0)) / (math.pi / 180.0)
        meter_y = meter_y * self.origin_shift / 180.0
        return meter_x, meter_y
