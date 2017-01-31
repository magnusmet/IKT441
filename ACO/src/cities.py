import json
from operator import itemgetter

byer = {}

from_city = None
to_city = None


def load_cities(filter_by_region=False, regions=(1, 2, 12, 4, 17)):
    if filter_by_region: filter_regions(regions)
    else:
        with open('norges_byer.json') as file:
            cities = json.load(file)
        subset = {}
        for city in cities:
            subset[city] = (cities[city][0], cities[city][1])
        global byer
        byer = dict(sorted(subset.items(), key=itemgetter(1)))


def filter_regions(regions):
    with open('norges_byer.json') as file:
        cities = json.load(file)
    subset = {}
    for city in cities:
        if cities[city][2] in regions:
            subset[city] = (cities[city][0], cities[city][1])
    global byer
    byer = dict(sorted(subset.items(), key=itemgetter(1)))


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

viable_cities = []


def get_next_city(avoid_cities, i):
    if len(avoid_cities) >= len(byer)+2:
        assert False
    if i == 0:
        global viable_cities
        viable_cities = [by for by in byer if by not in avoid_cities]
    return viable_cities[i]


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


def refine_dict():
    global byer
    d = {}
    for key in byer:
            a = key[0]
            b = key[1]
            d[a[0]] = a[1]
            d[b[0]] = b[1]
    byer = d
