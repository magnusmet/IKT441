from src.cities import load_cities_norway, load_all
from src.aco import aco

cities_to_visit = 5
ants = 3000*cities_to_visit

# load_cities_norway()
# aco('oslo', 'bergen', cities_to_visit, ants)

load_all()
aco('oslo', 'madrid', cities_to_visit, ants)
