from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Msg(models.Model):
    """
    Message model
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
    )

    latitude = models.FloatField(verbose_name="Latitude", default=-1)
    longitude = models.FloatField(verbose_name="Longitude", default=-1)
    is_cold = models.BooleanField(null=True)
    pm25_value = models.IntegerField(default=-1)
    is_health = models.BooleanField(null=True)

    city = models.CharField(max_length=20, null=True)

    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + '-' + self.date_added.__str__()
