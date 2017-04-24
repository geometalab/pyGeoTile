from pygeotile.point import Point

meter_x, meter_y, zoom = -9757148.442088600, 5138517.444985110, 19  # meters in Spherical Mercator EPSG:900913

point = Point.from_meters(meter_x=meter_x, meter_y=meter_y, zoom=zoom)

print('Pixels: ', point.pixels)  # Pixels:  (34430592, 49899136)
print('Lat/Lon: ', point.latitude_longitude)  # Lat/Lon:  (41.84987190947754, -87.64995574951166)
