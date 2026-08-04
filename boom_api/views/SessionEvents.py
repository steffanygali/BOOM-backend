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
from django.shortcuts import get_object_or_404
from django.utils import timezone



# cada actividad que se va realizando 
class SesionIniciarView(generics.CreateAPIView):
    serializer_class = SesionNinoSerializer
    permission_classes = (permissions.IsAuthenticated, EsPadre)

    def perform_create(self, serializer):
        nino = get_object_or_404(
            Nino, pk=self.request.data.get('nino_id'), padre__user=self.request.user
        )
        serializer.save(nino=nino, padre=self.request.user.padre)

#creamos la actividad
class RegistroActividadCreateView(generics.CreateAPIView):
    serializer_class = RegistroActividadSerializer
    permission_classes = (permissions.IsAuthenticated, EsPadre)

    def perform_create(self, serializer):
        sesion = get_object_or_404(
            SesionNino,
            pk=self.kwargs['sesion_id'],
            fin__isnull=True,          # solo se puede registrar en una sesión aún abierta
            padre__user=self.request.user,
        )
        serializer.save(sesion=sesion)

#cuando fianlize guradmos la ultima actividad 
class SesionFinalizarView(generics.UpdateAPIView):
    serializer_class = SesionNinoSerializer
    permission_classes = (permissions.IsAuthenticated, EsPadre)

    def get_queryset(self):
        return SesionNino.objects.filter(padre__user=self.request.user)

    def update(self, request, *args, **kwargs):
        sesion = self.get_object()
        registros = sesion.registros.all()

        sesion.fin = timezone.now()
        sesion.actividades_completadas = registros.filter(completada=True).count()
        sesion.tiempo_total_segundos = sum(r.tiempo_segundos for r in registros)
        sesion.save()

        return Response(self.get_serializer(sesion).data)