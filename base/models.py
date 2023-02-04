from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timesince
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Ride(models.Model):
    bus_company = models.CharField(max_length=100, blank=False, null=False)
    average_speed = models.PositiveSmallIntegerField(default=75)
    cities_where_collect_passengers = models.TextField(blank=False, null=False)
    is_express = models.BooleanField(default=False)
    price = models.PositiveSmallIntegerField(default=25)

    def __str__(self):
        stations_list = self.cities_where_collect_passengers.split(",")
        return '{} {} - {}'.format(self.bus_company, stations_list[0], stations_list[-1])

    def cities(self):
        return [city for city in self.cities_where_collect_passengers.split(',')]


class Ticket(models.Model):
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='tickets')
    bus = models.ForeignKey(Ride, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner}: {self.bus}; added: {self.bought()}'

    def holder(self):
        return self.owner.username

    def bus_credentials(self):
        stations_list = self.bus.cities_where_collect_passengers.split(",")
        return f'{self.bus.bus_company}: {stations_list[0]} - {stations_list[-1]}'

    def bought(self):
        return f'{timesince.timesince(self.date)} ago'
