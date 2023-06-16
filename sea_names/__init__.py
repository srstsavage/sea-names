"""Top-level package for sea-names."""

__author__ = """Luke Campbell"""
__email__ = "luke@axds.co"
__version__ = "0.1.0"

from .geo import get_region_polygons, get_sea_bounds, get_sea_name


__all__ = ["get_sea_bounds", "get_region_polygons", "get_sea_name"]
