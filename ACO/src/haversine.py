from math import radians, cos, sin, asin, sqrt
from src.cities import get_coords


def haversine(from_city, to_city):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lon1, lat1 = from_city[:2]
    lon2, lat2 = to_city[:2]
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


def get_distance(from_city, to_city):
    from_coord = get_coords(from_city)
    to_coord = get_coords(to_city)
    return haversine(from_coord, to_coord)