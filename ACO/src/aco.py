import random
from src.cities import get_next_city, get_number_of_cities, coarsen_dict,\
    refine_dict, set_end_cities, get_city, shorten_key, extend_key,\
    get_long_key, get_short_key, reduce, get_distance, plot
from time import time

traversed_edges = {}
best_score = 0
best_edges = []
shortest_distance = 0
pheromones_init = 1 # 100000


def roulette_wheel(visited_cities, start_city):
    number_of_cities = get_number_of_cities()

    viable_edges = [traversed_edges[edge] for edge in traversed_edges if edge[0] is start_city and edge[1] not in visited_cities]
    uncharted_edges = (number_of_cities - (len(visited_cities) + len(viable_edges))) * pheromones_init
    all_pheromones = sum(viable_edges) + uncharted_edges
    num = random.uniform(0, all_pheromones)
    s = 0
    i = 0
    selected_city = None
    while s <= num:
        selected_city = get_next_city(visited_cities, i)
        i += 1
        edge = (start_city, selected_city)
        try:
            s += traversed_edges[edge]
        except KeyError:
            s += pheromones_init
    return selected_city


class ANT:
    def __init__(self, city_a, city_b, cities_to_visit):
        self.visited_edges = {}
        self.visited_cities = {city_a, city_b}
        self.city_a = city_a
        self.city_b = city_b
        self.cities_to_visit = cities_to_visit + 2
        self.max_cost = 2*get_distance(city_a, city_b)

    def walk(self):
        current_city = self.city_a
        global traversed_edges
        while len(self.visited_cities) < self.cities_to_visit:
            prev_city = current_city
            current_city = roulette_wheel(self.visited_cities, prev_city)
            self.visited_edges[(prev_city, current_city)] = get_distance(prev_city, current_city)
            if (prev_city, current_city) not in traversed_edges:
                traversed_edges[(prev_city, current_city)] = pheromones_init
            self.visited_cities.add(current_city)
        self.visited_edges[(current_city, self.city_b)] = get_distance(current_city, self.city_b)
        if (current_city, self.city_b) not in traversed_edges:
            traversed_edges[(current_city, self.city_b)] = pheromones_init

    def pheromones(self):
        current_cost = self.get_distance_traveled()
        score = 1000 ** (1 - current_cost / self.max_cost)
        global traversed_edges
        global best_score
        global best_edges
        global shortest_distance
        if score > best_score:
            best_score = score
            best_edges = self.visited_edges
            shortest_distance = current_cost
        for edge in best_edges:
            traversed_edges[edge] += score
            if traversed_edges[edge] > 100000: traversed_edges[edge] = 100000

    def get_distance_traveled(self):
        return sum(self.visited_edges.values())


def reset():
    global traversed_edges
    global best_score
    global best_edges
    traversed_edges = {}
    best_score = 0
    best_edges = []


def refine_edges():
    global traversed_edges
    coarse_edges = get_long_key(traversed_edges)
    new_edges = {}
    for edge in coarse_edges:
        from_nodes = []
        to_nodes = []
        if coarse_edges[edge] < best_score/2: continue
        # Refined completely
        if isinstance(edge[0], str) and isinstance(edge[1], str):
            from_nodes.append(edge[0])
            to_nodes.append(edge[1])
        # City A is refined completely
        elif isinstance(edge[0], str):
            from_nodes.append(edge[0])
            to_nodes.append(edge[1][0])
            to_nodes.append(edge[1][1])
        # City B is refined completely
        elif isinstance(edge[1], str):
            from_nodes.append(edge[0][0])
            from_nodes.append(edge[0][1])
            to_nodes.append(edge[1])
        else:
            from_nodes.append(edge[0][0])
            from_nodes.append(edge[0][1])
            to_nodes.append(edge[1][0])
            to_nodes.append(edge[1][1])
        for from_node in from_nodes:
            a = from_node
            try:
                assert get_city(a)
            except KeyError:
                a = from_node[0]
                assert get_city(a)
            for to_node in to_nodes:
                b = to_node
                try:
                    assert get_city(b)
                except KeyError:
                    b = to_node[0]
                    assert get_city(b)
                new_edges[(a, b)] = coarse_edges[edge]
    reset()
    traversed_edges = new_edges


def aco(from_city, to_city, cities_to_visit, iterations=5000):
    direct_distance = get_distance(from_city, to_city)
    print('Direct path from', from_city, 'to', to_city, ':', direct_distance)
    t0 = time()
    reset()
    global traversed_edges
    set_end_cities(from_city, to_city)
    print('Reducing search space')
    reduce(cities_to_visit)
    coarse_level = 0
    print('Coarsening search space')
    while get_number_of_cities() > 30:
        coarsen_dict()
        coarse_level += 1
    if coarse_level > 0: shorten_key()
    while coarse_level > 0:
        print('Starting on coarse level:', coarse_level)
        print(get_number_of_cities(), 'nodes in search space')

        release_ants(from_city, to_city, cities_to_visit, iterations)

        print('Refining search space')
        extend_key()
        refine_dict()
        refine_edges()

        if coarse_level > 1:
            shorten_key()
            traversed_edges = get_short_key(traversed_edges)
        coarse_level -= 1

    print('Starting on coarse level:', coarse_level)
    print(get_number_of_cities(), 'nodes in search space')

    release_ants(from_city, to_city, cities_to_visit, iterations)

    path = [place[0] for place in best_edges]+[to_city]
    print(path)
    print('Path distance:', shortest_distance)
    print('Direct path from', from_city, 'to', to_city, ':', direct_distance)
    print('Time passed', time() - t0, 'sec')
    # plot([place[0] for place in best_edges]+[to_city])


def release_ants(from_city, to_city, cities_to_visit, iterations):
    t0 = time()
    for i in range(iterations):
        ant = ANT(from_city, to_city, cities_to_visit)
        ant.walk()
        ant.pheromones()
        if i % 1000 == 0:
            print(i, ':', shortest_distance)

    print(time() - t0, shortest_distance)

