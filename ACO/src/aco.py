import random
from src.haversine import getDistance
from src.cities import getRandomCity, getNumberOfCities
from time import time

traversed_edges = {}
number_of_cities = getNumberOfCities()
MAXPHERMONES = 100000
best_score = 0
best_edges = []
shortest_distance = 0

def rouletteWheel(visited_cities, start_city):
    global traversed_edges
    global number_of_cities
    avoid_cities = visited_cities.copy()

    viable_edges = [traversed_edges[edge] for edge in traversed_edges if edge[0] is start_city and edge[1] not in visited_cities]
    uncharted_edges = (number_of_cities - (len(visited_cities) + len(viable_edges)))*MAXPHERMONES
    all_phermones = sum(viable_edges) + uncharted_edges
    num = random.uniform(0, all_phermones)
    s = 0
    selected_city = None
    i = 0
    while s <= num:
        selected_city = getRandomCity(avoid_cities)
        avoid_cities.add(selected_city)
        edge = (start_city, selected_city)
        try:
            s += traversed_edges[edge]
        except KeyError:
            s += MAXPHERMONES
    return selected_city


class ANT:
    def __init__(self, city_a, city_b, cities_to_visit):
        self.visited_edges = {}
        self.visited_cities = {city_a, city_b}
        self.city_a = city_a
        self.city_b = city_b
        self.cities_to_visit = cities_to_visit + 2
        self.max_cost = 100 + cities_to_visit*(calcCost(city_a, city_b))

    def walk(self):
        current_city = self.city_a
        global traversed_edges
        while len(self.visited_cities) < self.cities_to_visit:
            prev_city = current_city
            current_city = rouletteWheel(self.visited_cities, prev_city)
            self.visited_edges[(prev_city, current_city)] = calcCost(prev_city, current_city)
            if (prev_city, current_city) not in traversed_edges:
                traversed_edges[(prev_city, current_city)] = MAXPHERMONES
            self.visited_cities.add(current_city)
        self.visited_edges[(current_city, self.city_b)] = calcCost(current_city, self.city_b)
        if (current_city, self.city_b) not in traversed_edges:
            traversed_edges[(current_city, self.city_b)] = MAXPHERMONES

    def phermones(self):
        current_cost = sum(self.visited_edges.values())
        score = 1000 ** (1 - current_cost / self.max_cost)
        global traversed_edges
        global best_score
        global best_edges
        global shortest_distance
        if score > best_score:
            best_score = score
            best_edges = self.visited_edges
            shortest_distance = current_cost
            print(shortest_distance, self.city_a,[place[0] for place in best_edges.keys()][1:], self.city_b)
        for edge in best_edges:
            traversed_edges[edge] += score
            if traversed_edges[edge] > 10000:
                traversed_edges[edge] = 10000

    def getDistanceTraveled(self):
        return sum(self.visited_edges.values())

def calcCost(a, b):
    return getDistance(a, b)

def evaporate():
    global traversed_edges
    global MAXPHERMONES
    MAXPHERMONES *= 0.99
    for edge in traversed_edges:
        traversed_edges[edge] *= 0.99
        if traversed_edges[edge] < 1:
            traversed_edges[edge] = 1

def releaseAnts(from_city, to_city, cities_to_visit, iterations=100000):
    t0 = time()
    ant = None
    ants_on_same_path = 0
    for i in range(iterations):
        evaporate()
        ant = ANT(from_city, to_city, cities_to_visit)
        ant.walk()
        ant.phermones()
        # if i % 200 == 0:
            # print(i, ant.getDistanceTraveled(), [place[0] for place in ant.visited_edges.keys()])
        #     print(ants_on_same_path)
        #     print(shortest_distance, [place[0] for place in best_edges.keys()])
        if ant.getDistanceTraveled() == shortest_distance:
            ants_on_same_path += 1
            if ants_on_same_path > 200:
                print('Converged on optimal path after', time() - t0, 'sec')
                break
        elif ants_on_same_path > 1:
            ants_on_same_path -= 1
    # return ant.getDistanceTraveled(), [place[0] for place in ant.visited_edges.keys()][1:]
    # return [place[0] for place in ant.visited_edges.keys()][1:]

# for i in range(10000):
#     ant = ANT()
#     ant.walk(a)
#     ant.pheromones()
#     print(i, getSum(ant.visitedEdges))
