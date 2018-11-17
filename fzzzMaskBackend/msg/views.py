from rest_framework import viewsets, permissions

from .serializers import *


# Create your views here.
class MsgViewSet(viewsets.ModelViewSet):
    queryset = Msg.objects.all()
    serializer_class = MsgSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

