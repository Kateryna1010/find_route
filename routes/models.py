from django.core.exceptions import ValidationError
from django.db import models

from cities.models import City
from trains.models import Train


class Route(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Route name')
    travel_time = models.PositiveSmallIntegerField(verbose_name='Total travel time')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='route_from_city_set', verbose_name='From')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='route_to_city_set', verbose_name='To')
    trains = models.ManyToManyField('trains.Train', verbose_name='List of trains')

    def __str__(self):
        return f'Route {self.name} from {self.from_city}'

    class Meta:
        ordering = ['travel_time']


