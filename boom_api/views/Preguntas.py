from django.db.models import *
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from boom_api.models import *
from boom_api.permissions import *
from boom_api.serializers import *


# get para obtener preguntas
class PreguntaEvaluacionListView(generics.ListAPIView):
    queryset = PreguntaEvaluacion.objects.filter(activo=True)
    serializer_class =  PreguntaEvaluacionSerializer
    permission_classes = (permissions.IsAuthenticated,)

# para crear solo actua como un post

class EvaluacionInicialCreateView(generics.CreateAPIView):
    serializer_class = EvaluacionInicialSerializer
    permission_classes = (permissions.IsAuthenticated, EsPadre)

    def perform_create(self, serializer):
        nino_id = self.request.data.get('nino_id') or self.request.data.get('nino')
        nino = get_object_or_404(
            Nino, pk=nino_id, padre__user=self.request.user
        )
        serializer.save(nino=nino, padre=self.request.user.padre)

class RespuestaNinoCreateView(generics.CreateAPIView):
    serializer_class = RespuestaNinoSerializer
    permission_classes = (permissions.IsAuthenticated, EsPadre)

    def perform_create(self, serializer):
        evaluacion = get_object_or_404(
            EvaluacionInicial,
            pk=self.kwargs['evaluacion_id'],
            completada=False,
            padre__user=self.request.user,
        )
        serializer.save(evaluacion=evaluacion)

#un update sencillito

class EvaluacionInicialFinalizarView(generics.UpdateAPIView):
    queryset = EvaluacionInicial.objects.all()
    serializer_class = EvaluacionInicialSerializer
    permission_classes = (permissions.IsAuthenticated, EsPadre)

    def get_queryset(self):
        return EvaluacionInicial.objects.filter(padre__user=self.request.user)

    def update(self, request, *args, **kwargs):
        evaluacion = self.get_object()
        evaluacion.completada = True
        evaluacion.fecha_fin = timezone.now()
        evaluacion.save()
        return Response(self.get_serializer(evaluacion).data)
