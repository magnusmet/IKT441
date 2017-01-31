from src.cities import load_cities
from src.aco import aco

load_cities(filter_by_region=True)
aco('oslo', 'grimstad', 2)
