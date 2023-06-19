"""Determine the NCEI Sea Name from a point."""
import re
import tarfile

from functools import lru_cache
from typing import Dict, List, Optional, Tuple

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from sea_names.cache import CACHE_BOUNDS_FILE, CACHE_FILE, download_sea_names


@lru_cache
def get_sea_bounds() -> Dict[str, Polygon]:
    """Return a mapping of the sea name to the bounding polygon."""
    if not (CACHE_BOUNDS_FILE.exists() and CACHE_FILE.exists()):
        download_sea_names()

    name: Optional[str] = None

    with open(CACHE_BOUNDS_FILE, "r") as f:
        points: List[Tuple[float, float]] = []
        polygons: Dict[str, Polygon] = {}

        for line_no, line in enumerate(f.readlines()):
            line = line.strip()  # strip newline
            line = line.replace("  ", " ")
            if not line:
                continue
            if line.startswith("> "):
                if name and line_no > 0:
                    polygon = Polygon(points)
                    polygons[name] = polygon
                # Name marker
                name = line[2:]
                points = []
            else:
                # Point details
                x, y = [float(i) for i in line.split(" ")]
                points.append((x, y))
        if name:
            polygon = Polygon(points)
            polygons[name] = polygon

    return polygons


def get_region_polygons(region_name: str) -> List[Polygon]:
    """Return the list of polygons for the given NCEI Sea Name (Region)."""
    if not (CACHE_BOUNDS_FILE.exists() and CACHE_FILE.exists()):
        download_sea_names()
    polygons = []
    with tarfile.open(CACHE_FILE) as tf:
        if tf is None:
            raise ValueError("unknown tarfile open error")

        f = tf.extractfile(f"sea_names/{region_name}.polygons")
        if f is None:
            raise ValueError("Failed to extract region, (unknown error)")
        with f:
            buf = f.read().decode("utf-8")
            lines = buf.split("\n")
            points: List[Tuple[float, float]] = []

            for line_no, line in enumerate(lines):
                line = line.strip()  # strip newline
                line = line.replace("  ", " ")
                if not line:
                    continue
                if line.startswith(">"):
                    if line_no > 0:
                        polygon = Polygon(points)
                        polygons.append(polygon)
                    # Name marker
                    points = []
                else:
                    # Point details
                    x, y = [float(i) for i in line.split(" ")]
                    points.append((x, y))
            polygon = Polygon(points)
            polygons.append(polygon)
    return polygons


def get_sea_name(*args) -> Optional[str]:
    """Return the first sea name that the point intersects."""
    if len(args) == 2:
        point = Point(*args)
    elif len(args) == 1 and isinstance(args[0], Point):
        point = args
    elif len(args) == 1 and isinstance(args[0], tuple):
        point = Point(*args[0])
    else:
        raise ValueError("Unable to determine point from function arguments.")

    polygons = get_sea_bounds()
    for name, bounds in polygons.items():
        if bounds.contains(point):
            for polygon in get_region_polygons(name):
                if polygon.contains(point):
                    tokens = name.split(" ")
                    if re.match(r"[0-9]+[a-z]?", tokens[-1]):
                        name = " ".join(tokens[:-1])
                    return name
    return None
