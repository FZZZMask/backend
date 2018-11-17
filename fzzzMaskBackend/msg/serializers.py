from rest_framework import serializers
from .models import Msg


class MsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Msg
        fields = (
            'pk',
            'user',
            'latitude',
            'longitude',
            'is_cold',
            'pm25_value',
            'is_health',
            'date_added',
            'last_added'
        )


