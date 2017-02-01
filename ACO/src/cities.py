import json
from operator import itemgetter
from math import radians, cos, sin, asin, sqrt
from matplotlib import pyplot as plt

byer = {}

from_city = None
to_city = None
long_key = {} # Keys for multilevel context
short_key = {} # Integer keys to speed up lookup
trans_long_short = {} # Translator for long key to short key
trans_short_long = {} # Translator for short key to long key


# Load all cities
def load_all():
    with open('cities.json') as file:
        cities = json.load(file)
    subset = {}
    for country in cities:
        for city in cities[country]:
            if city == 'madrid' and not country == 'es': continue
            subset[city] = (cities[country][city][0], cities[country][city][1])
    global byer
    byer = dict(sorted(subset.items(), key=itemgetter(1)))


def load_cities_norway():
    with open('norges_byer.json') as file:
        cities = json.load(file)
    subset = {}
    for city in cities:
        subset[city] = (cities[city][0], cities[city][1])
    global byer
    byer = dict(sorted(subset.items(), key=itemgetter(1)))


# Removes from_city and to_city from the rest and stores in variable
def set_end_cities(city_a, city_b):
    global from_city
    global to_city
    if from_city and to_city:
        byer[from_city[0]] = from_city[1]
        byer[to_city[0]] = to_city[1]
    from_city = (city_a, byer[city_a])
    to_city = (city_b, byer[city_b])
    byer.pop(city_a)
    byer.pop(city_b)


viable_cities = [] # Stores cities for quick iteration


def get_next_city(avoid_cities, i):
    if len(avoid_cities) >= len(byer)+2:
        assert False
    if i == 0:
        global viable_cities
        viable_cities = [by for by in byer if by not in avoid_cities]
    return viable_cities[i]


# Get city with coordinates, often used to assert city names are valid
def get_city(city):
    if city is from_city[0]:
        return from_city
    elif city is to_city[0]:
        return to_city
    return city, tuple(byer[city])


def get_coords(city):
    try:
        if city is from_city[0]:
            return from_city[1]
        elif city is to_city[0]:
            return to_city[1]
    except TypeError:
        pass
    return byer[city]


def get_number_of_cities():
    return len(byer)+2


# Groups cities together for multilevel approach
def coarsen_dict():
    global byer
    d_copy = list(byer.items())
    clusters = {}
    while len(clusters) < len(byer)/2:
        a = d_copy.pop()
        try:
            b = d_copy.pop()
            cluster = ((a,b), ((a[1][0]+b[1][0])/2 , (a[1][1]+b[1][1])/2))
            clusters[cluster[0]] = cluster[1]
        except IndexError:
            clusters[(a,a)] = (a[1][0], a[1][1])
    byer = clusters


# Splits groups of cities
def refine_dict():
    global byer
    d = {}
    for key in byer:
            a = key[0]
            b = key[1]
            d[a[0]] = a[1]
            d[b[0]] = b[1]
    byer = d


# Makes integer keys for fast lookup
def shorten_key():
    global long_key
    global byer
    global trans_long_short
    global trans_short_long
    trans_long_short = {}
    trans_short_long = {}
    long_key = byer
    i = 0
    sk = {}
    for node in long_key:
        sk[i] = long_key[node]
        trans_short_long[i] = node
        trans_long_short[node] = i
        i += 1
    global short_key
    short_key = sk
    byer = sk


# Returns to long key for multilevel grouping context
def extend_key():
    global byer
    byer = long_key


def get_long_key(keys):
    return_keys = {}
    for key in keys:
        a = key[0]
        if isinstance(a, int):
            a = trans_short_long[a]
        b = key[1]
        if isinstance(b, int):
            b = trans_short_long[b]
        return_keys[(a,b)] = keys[key]
    return return_keys


def get_short_key(keys):
    return_keys = {}
    for key in keys:
        a = key[0]
        if not isinstance(a, str):
            a = trans_long_short[a]
        b = key[1]
        if not isinstance(b, str):
            b = trans_long_short[b]
        return_keys[(a,b)] = keys[key]
    return return_keys


# Reduces search space by eliminating cities far from line between from_city and to_city
def reduce(cities_to_visit, n=None):
    try: assert from_city and to_city and ((not n) or n > 3)
    except: return
    if not n:
        n = get_distance(from_city[0], to_city[0])/15
        if n < 4: n = 0
        n = int(n)
    y1 = from_city[1][0]
    y2 = to_city[1][0]
    x1 = from_city[1][1]
    x2 = to_city[1][1]
    if x1 < x2 and n > 0:
        delta_x = (x2 - x1) / n
        lat = [x1 + (i * delta_x) for i in range(1, n)]
        if y1 < y2:
            delta_y = (y2 - y1) / n
            lon = [y1 + (i * delta_y) for i in range(1, n)]
        else:
            delta_y = (y2 - y1) / n
            lon = [y2 + (i * delta_y) for i in range(1, n)]
            lon.reverse()
    elif n > 0:
        delta_x = (x1 - x2) / n
        lat = [x2 + (i * delta_x) for i in range(1, n)]
        if y1 < y2:
            delta_y = (y2 - y1) / n
            lon = [y1 + (i * delta_y) for i in range(1, n)]
            lon.reverse()
        else:
            delta_y = (y1 - y2) / n
            lon = [y2 + (i * delta_y) for i in range(1, n)]
    mid_points = []
    if n > 0: mid_points = [(lon[i], lat[i]) for i in range(n - 1)]

    global byer
    subset = {}
    try:
        radius = get_distance(from_city[0], to_city[0]) / (n / 2)
    except ZeroDivisionError:
        radius = 5*cities_to_visit
    for city in byer:
        if get_distance(from_city[0], city) < radius:
            subset[city] = byer[city]
        elif get_distance(city, to_city[0]) < radius:
            subset[city] = byer[city]
        else:
            for mid_point in mid_points:
                if haversine(get_coords(city), mid_point) < radius:
                    subset[city] = byer[city]
                    break
    all_cities = len(byer)
    if len(subset) <= cities_to_visit*6 and n > 3: reduce(cities_to_visit, n-5)
    else:
        byer = subset
        print('reduced from', all_cities, 'cities to', len(byer), 'cities')


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


def plot(visited):
    lats = [byer[city][1] for city in byer]
    lons = [byer[city][0] for city in byer]
    plt.plot(lats, lons, 'ro')

    lats = [get_coords(city)[1] for city in visited]
    lons = [get_coords(city)[0] for city in visited]
    plt.plot(lats, lons)

    plt.show()
