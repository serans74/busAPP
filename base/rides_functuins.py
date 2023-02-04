# list of lists to flat list
from base.models import Ride


def flatten(xss):
    return [x for xs in xss for x in xs]


# all cities that we cover with our routes
def cities_list():
    all_cities_without_repetitions = []
    rides = [route.cities_where_collect_passengers.split(',') for route in Ride.objects.all()]
    flat_list = flatten(rides)
    for route in flat_list:
        if route not in all_cities_without_repetitions:
            all_cities_without_repetitions.append(route)

    return sorted(all_cities_without_repetitions)


def check_bus_route(bus, start, stop):
    cities_in_route = bus.cities_where_collect_passengers
    if str(start) in cities_in_route and str(stop) in cities_in_route:
        if cities_in_route.index(start) < cities_in_route.index(stop):
            return True
    return False


def all_to_city(bus, end):
    cities_in_route = bus.cities_where_collect_passengers.split(',')
    if str(end) in cities_in_route and cities_in_route.index(end) != 0:
        return True
    return False


def all_from_city(bus, start):
    cities_in_route = bus.cities_where_collect_passengers.split(',')
    if start in cities_in_route and cities_in_route.index(start) != len(cities_in_route) - 1:
        return True
    return False
