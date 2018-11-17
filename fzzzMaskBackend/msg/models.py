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
        null=False
    )

    latitude = models.FloatField(verbose_name="Latitude", default=0)
    longitude = models.FloatField(verbose_name="Longitude", default=0)
    is_cold = models.BooleanField(default=False)
    pm25_value = models.IntegerField(default=-1)
    is_health = models.BooleanField(default=False)

    date_added = models.DateTimeField(auto_now_add=True)
    last_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + '-' + self.date_added
