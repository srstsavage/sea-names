"""Module for evaluating the sea names of all points in a trajectory."""
from typing import List

import numpy as np

from shapely.geometry import Point


def evaluate_possible_regions(
    sea_bounds: dict, lon: np.ndarray, lat: np.ndarray
) -> List[str]:
    """Return a list of seas where the trajectory intersects the bbox."""
    names = list(sea_bounds.keys())
    all_bounds = np.array([i.bounds for i in sea_bounds.values()])
    LONS, _ = np.meshgrid(lon, np.ones(len(all_bounds)))
    LATS, _ = np.meshgrid(lat, np.ones(len(all_bounds)))

    left = LONS < all_bounds[:, 0][:, None]
    right = LONS > all_bounds[:, 2][:, None]
    below = LATS < all_bounds[:, 1][:, None]
    above = LATS > all_bounds[:, 3][:, None]

    solution = (~(left | right)) & (~(above | below))

    possible_regions = []
    for i, value in enumerate(np.sum(solution, axis=1) > 0):
        if value:
            possible_regions.append(names[i])
    return possible_regions


def evaluate_polygon_brute_force(
    possible_regions: List[str], lon: np.ndarray, lat: np.ndarray
) -> List[str]:
    """Return the definitive list of regions that intersect that trajectory

    This function evaluates the polygons of each region compared to each point of the trajectory in
    a slow brute-force manner. The fewer the number of possible regions the better this will
    perform.
    """
    from sea_names.geo import get_region_polygons

    valid_regions = []
    for region in possible_regions:
        region_is_valid = False
        for j, polygon in enumerate(get_region_polygons(region)):
            if region_is_valid:
                break
            for i in range(len(lon)):
                point = Point(lon[i], lat[i])
                if polygon.contains(point):
                    region_is_valid = True
                    valid_regions.append(region)
                    break
    return valid_regions
