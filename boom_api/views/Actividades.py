from django.db.models import *
from django.db import transaction
from django.views import generic
from boom_api.models import Profiles
from boom_api.permissions import *
from boom_api.serializers import UserSerializer
from boom_api.serializers import *
from boom_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from drf_spectacular.utils import extend_schema


class ActividadListView(generics.ListAPIView):
    queryset = Actividad.objects.filter(activo=True)
    serializer_class = ActividadSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ActividadViewSet(generics.CreateAPIView):
    queryset = Actividad.objects.filter(activo=True)
    serializer_class = ActividadSerializer
    permission_classes = (permissions.IsAuthenticated, EsDocenteOTerapeutaOAdmin)

class ActividadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Actividad.objects.filter(activo=True)
    serializer_class = ActividadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [permissions.IsAuthenticated(), EsDocenteOTerapeutaOAdmin()]
        return [permissions.IsAuthenticated()]
