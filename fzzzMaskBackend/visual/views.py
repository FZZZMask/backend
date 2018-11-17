from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from msg.models import Msg


# Create your views here.
@api_view(['GET'])
def health(request, *args, **kwargs):
    """
    突发死亡监测
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
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
        base_url = "https://restapi.amap.com/v3/geocode/regeo?key=948049944349c5ffc8cebcb4e1efb1c3&location="
        url = base_url + str(lng) + ',' + str(lat)
        r = requests.get(url).json()
        print(r)
        city = r.get("regeocode").get("addressComponent").get("city")
        # city = r["regeocode"]["addressComponent"]["city"]
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
    print(accidents)
    for accident in accidents:
        city = None
        if accident.city is None:
            city = coordinate2city(accident.latitude, accident.longitude)
            accident.city = city
            accident.save()
        else:
            city = accident.city

        print(city)
        if city is not None and health_dict.get(city) is not None:
            print("Plus 1")
            health_dict[city] += 1

    return Response(health_dict, status=status.HTTP_200_OK)


@api_view(['GET'])
def pm25(request):
    """
    PM 2.5 区域数据
    :param request:
    :return:
    """
    now = datetime.now()
    frontier = now

    granularity = request.GET.get('granularity', None)
    if granularity == "weekly":
        frontier = now - relativedelta(weeks=1)
    elif granularity == "daily":
        frontier = now - relativedelta(days=1)
    else:  # return "hourly"
        frontier = now - relativedelta(hours=1)

    pm25_values = Msg.objects.filter(date_added__range=(frontier, now),
                                     pm25_value__isnull=False)

    data_list = list()

    for i in range(50):  # y
        for j in range(50):  # x
            data_list.append([j, i, 0])

    max_value = 0
    for pm25_value in pm25_values:
        x = int((pm25_value.longitude - 118.46) // 0.0114)
        y = int((pm25_value.latitude - 31.58) // 0.0094)
        value = pm25_value.pm25_value

        count = y * 50 + x
        print(count, x, y)
        if 0 <= count < 2500:
            data_list[count][2] += value
            max_value = max(data_list[count][2], max_value)  # largest sum

    for data_elem in data_list:
        if max_value != 0:
            level = ((6 * data_elem[2]) // max_value)
        else:
            level = 0

        if level >= 6:
            level = 5

        # Reverse
        level = 5 - level

        data_elem[2] = level

    data = {"data": data_list}

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def cold(request):
    """
    感冒区域数据
    :param request:
    :return:
    """

    now = datetime.now()
    frontier = now

    granularity = request.GET.get('granularity', None)
    if granularity == "monthly":
        frontier = now - relativedelta(months=1)
    elif granularity == "weekly":
        frontier = now - relativedelta(weeks=1)
    else:  # return "daily"
        frontier = now - relativedelta(days=1)

    cold_patients = Msg.objects.filter(date_added__range=(frontier, now),
                                       is_cold=True)

    print(cold_patients)

    data_list = list()

    for i in range(50):  # y
        for j in range(50):  # x
            data_list.append([j, i, 0])

    max_value = 0
    for cold_patient in cold_patients:
        x = int((cold_patient.longitude - 118.46) // 0.0114)
        y = int((cold_patient.latitude - 31.58) // 0.0094)

        count = y * 50 + x
        # print(count, x, y)
        if 0 <= count < 2500:
            data_list[count][2] += 1
            max_value = max(data_list[count][2], max_value)

    for data_elem in data_list:
        if max_value != 0:
            level = ((6 * data_elem[2]) // max_value)
        else:
            level = 0

        if level >= 6:
            level = 5

        # Reverse
        level = 5 - level
        # 5 is the worst, 0 is the best.

        data_elem[2] = level

    data = {"data": data_list}

    return Response(data, status=status.HTTP_200_OK)
