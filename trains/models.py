from django.core.exceptions import ValidationError
from django.db import models

from cities.models import City


class Train(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Train number')
    travel_time = models.PositiveSmallIntegerField(verbose_name='Travel time')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='from_city_set', verbose_name='From')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='to_city_set', verbose_name='To')

    def __str__(self):
        return f'Train №{self.name} from {self.from_city} to {self.to_city}'

    class Meta:
        ordering = ['travel_time']

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError('Field "From" is equal to field "To"')
        qs = Train.objects.filter(travel_time=self.travel_time,
                                  from_city=self.from_city,
                                  to_city=self.to_city).exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError('Such train already exists')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

