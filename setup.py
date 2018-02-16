from io import open
from setuptools import setup, find_packages

with open('README.rst', 'rb') as f:
    readme = f.read().decode('utf-8')

setup(
    name='pyGeoTile',
    version='1.0.4',
    description='Python package to handle tiles and points of different projections, in particular WGS 84 '
                '(Latitude, Longitude), Spherical Mercator (Meters), Pixel Pyramid and Tiles (TMS, Google, QuadTree)',
    long_description=readme,
    author='Samuel Kurath',
    author_email='geometalab@hsr.ch',
    url='https://github.com/geometalab/pyGeoTile',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs'))
)
