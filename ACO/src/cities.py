import json
from random import choice

with open('norges_byer.json') as file:
    byer = json.load(file)

fylker = (1,2,12,4,17)
subset = {}
for by in byer:
    if byer[by][2] in fylker:
        subset[by] = byer[by]

byer = subset

print(len(byer))
#print(len(byer), byer)


def getRandomCity(visited_cities):
    assert len(byer) > len(visited_cities)
    while True:
        city = choice(list(byer.keys()))
        if city not in visited_cities:
            return city


def getCity(city):
    return city, tuple(byer[city])


def getCoord(city):
    return byer[city]


def getNumberOfCities():
    return len(byer)
