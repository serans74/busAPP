from base.views import all_from_city, all_to_city, check_bus_route
from django.test import TestCase
from base.models import Ride


def create_test_rides():
    Ride.objects.create(bus_company='dummy Company', cities_where_collect_passengers='Krakow,Warszawa,Gdynia,Gdansk',
                        is_express=True, price=230)
    Ride.objects.create(bus_company='dummier Company', average_speed=97,
                        cities_where_collect_passengers='Sanok,Rzeszow,Radom,Warszawa', is_express=False)
    Ride.objects.create(bus_company='even dummier Company', average_speed=50,
                        cities_where_collect_passengers='Hel,Jastarnia,Gdynia,Gdansk,Warszawa', price=2137)


class RideTestCase(TestCase):
    def setUp(self):
        create_test_rides()

    def test_creating_rides(self):
        first_bus = Ride.objects.get(bus_company='dummy Company')
        second_bus = Ride.objects.get(bus_company='dummier Company')
        third_bus = Ride.objects.get(bus_company='even dummier Company')

        self.assertEqual(first_bus.bus_company, 'dummy Company')
        self.assertEqual(second_bus.bus_company, 'dummier Company')
        self.assertEqual(third_bus.bus_company, 'even dummier Company')

        self.assertEqual(first_bus.average_speed, 75)
        self.assertEqual(second_bus.average_speed, 97)
        self.assertEqual(third_bus.average_speed, 50)

        self.assertEqual(first_bus.cities_where_collect_passengers, 'Krakow,Warszawa,Gdynia,Gdansk')
        self.assertEqual(second_bus.cities_where_collect_passengers.split(','),
                         ['Sanok', 'Rzeszow', 'Radom', 'Warszawa'])
        self.assertEqual(len(third_bus.cities_where_collect_passengers.split(',')), 5)

        self.assertEqual(first_bus.is_express, True)
        self.assertEqual(second_bus.is_express, False)
        self.assertEqual(second_bus.is_express, False)

        self.assertEqual(first_bus.price, 230)
        self.assertEqual(second_bus.price, 25)
        self.assertEqual(third_bus.price, 2137)


class CheckBusRouteTestCase(TestCase):
    def setUp(self):
        create_test_rides()

    def test_check_bus_route(self):
        first_bus = Ride.objects.get(bus_company='dummy Company')
        second_bus = Ride.objects.get(bus_company='dummier Company')
        third_bus = Ride.objects.get(bus_company='even dummier Company')

        self.assertEqual(check_bus_route(first_bus, 'Krakow', 'Gdynia'), True)
        self.assertEqual(check_bus_route(second_bus, 'Radom', 'Warszawa'), True)
        self.assertEqual(check_bus_route(third_bus, 'Gdansk', 'Jastarnia'), False)

        self.assertEqual(check_bus_route(first_bus, 'Sanok', 'Rybik'), False)

        self.assertEqual(check_bus_route(third_bus, 1234, True), False)


class AllToCityTestCase(TestCase):
    def setUp(self):
        create_test_rides()

    def test_all_to_city(self):
        first_bus = Ride.objects.get(bus_company='dummy Company')
        second_bus = Ride.objects.get(bus_company='dummier Company')
        third_bus = Ride.objects.get(bus_company='even dummier Company')

        self.assertEqual(all_to_city(first_bus, 'Warszawa'), True)
        self.assertEqual(all_to_city(first_bus, 'Gdansk'), True)
        self.assertEqual(all_to_city(first_bus, 'Krakow'), False)

        self.assertEqual(all_to_city(second_bus, 'Sanok'), False)
        self.assertEqual(all_to_city(second_bus, 'Jastarnia'), False)

        self.assertEqual(all_to_city(third_bus, 2137), False)


class AllFromCityTestCase(TestCase):
    def setUp(self):
        create_test_rides()

    def test_all_from_city(self):
        first_bus = Ride.objects.get(bus_company='dummy Company')
        second_bus = Ride.objects.get(bus_company='dummier Company')
        third_bus = Ride.objects.get(bus_company='even dummier Company')

        self.assertEqual(all_from_city(third_bus, 'Hel'), True)
        self.assertEqual(all_from_city(third_bus, 'Jastarnia'), True)
        self.assertEqual(all_from_city(third_bus, 'Warszawa'), False)

        self.assertEqual(all_from_city(second_bus, 'Warszawa'), False)
        self.assertEqual(all_from_city(second_bus, 'Rybnik'), False)

        self.assertEqual(all_from_city(first_bus, 69420), False)