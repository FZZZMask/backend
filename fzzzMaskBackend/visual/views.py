from datetime import datetime

from dateutil.relativedelta import relativedelta
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

import requests
from msg.models import Msg


# Create your views here.
class VisualViewSet(viewsets.ViewSet):
    queryset = Msg.objects.order_by('date_added')
    permission_classes = [
        permissions.AllowAny
    ]

    def health(self, request, *args, **kwargs):
        now = datetime.now()
        frontier = now

        granularity = request.GET.get('granularity', None)
        if granularity == "monthly":
            frontier = now - relativedelta(months=1)
        elif granularity == "weekly":
            frontier = now - relativedelta(weeks=1)
        else:  # return "daily"
            frontier = now - relativedelta(days=1)

        accidents = Msg.objects.filter(date_added__range=(frontier, now),
                                       is_health=False)

        def coordinate2city(lat, lng):
            base_url = "ttps://restapi.amap.com/v3/geocode/regeo?key=948049944349c5ffc8cebcb4e1efb1c3&location="
            url = base_url + str(lng) + ',' + str(lat)
            r = requests.get(url).json()
            city = r.get("regeocodes").get("addressComponent").get("city")
            if city is None:
                return None
            else:
                return city


        health_dict = {
            "南京市": 0,
            "无锡市": 0,
            "徐州市": 0,
            "常州市": 0,
            "苏州市": 0,
            "南通市": 0,
            "连云港市": 0,
            "淮安市": 0,
            "盐城市": 0,
            "扬州市": 0,
            "镇江市": 0,
            "泰州市": 0,
            "宿迁市": 0,
        }

        for accident in accidents:
            city = None
            if accident.city is None:
                city = coordinate2city(accident.latitude, accident.longitude)
                accident.city = city
                accident.save()
            else:
                city = accident.city

            if city is not None and health_dict.get(city):
                health_dict[city] += 1

        return Response(health_dict, status=status.HTTP_200_OK)



