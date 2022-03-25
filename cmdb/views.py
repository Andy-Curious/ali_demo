from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Host, CloudHost
from .serializers import HostSerializer, CloudHostSerializer
from .tasks import ali_cloud_info_collect


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class CloudHostViewSet(viewsets.ModelViewSet):
    queryset = CloudHost.objects.all()
    serializer_class = CloudHostSerializer


class CeleryTestView(APIView):

    def get(self, request, *args, **kwargs):
        ali_cloud_info_collect()
        data = {
            "data": 123
        }

        return Response(data, status=status.HTTP_200_OK)
