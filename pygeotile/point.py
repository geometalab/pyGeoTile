import math


class Point:
    def __init__(self, tile_size=256, earth_radius=6378137):
        super().__init__()
        self._latitude = None
        self._longitude = None
        self._zoom = None
        self._tile_size = tile_size
        self._earth_radius = earth_radius

    @classmethod
    def from_coordinates(cls, latitude=0.0, longitude=0.0):
        point = cls()
        point.coordinates = (latitude, longitude)
        return point

    @classmethod
    def from_pixel(cls, pixel_x=0, pixel_y=0, zoom=0):
        point = cls()
        point.zoom = zoom
        meter_x = pixel_x * point.resolution - point.origin_shift
        meter_y = pixel_y * point.resolution - point.origin_shift
        return point.from_meters(meter_x=meter_x, meter_y=meter_y)

    @classmethod
    def from_meters(cls, meter_x=0, meter_y=0.0):
        point = cls()
        longitude = (meter_x / point.origin_shift) * 180.0
        latitude = (meter_y / point.origin_shift) * 180.0
        latitude = 180 / math.pi * (2 * math.atan(math.exp(latitude * math.pi / 180.0)) - math.pi / 2.0)
        return point.from_coordinates(latitude=latitude, longitude=longitude)

    @property
    def coordinates(self):
        return self._latitude, self._longitude

    @coordinates.setter
    def coordinates(self, value):
        if type(value) is tuple:
            latitude, longitude = value
            self._latitude = latitude
            self._longitude = longitude
        else:
            raise TypeError('Arguments of coordinates needs to a tuple of Latitude and Longitude!')

    @property
    def pixels(self):
        """Gets pixels of the EPSG:4326 pyramid by a specific zoom"""
        latitude, longitude = self.coordinates
        pixel_x = (180 + latitude) / self.resolution
        pixel_y = (90 + longitude) / self.resolution
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

    @property
    def zoom(self):
        # TODO Attribute Error or something similar if zoom is None
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
