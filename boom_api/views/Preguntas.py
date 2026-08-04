from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from boom_api.models import EvaluacionInicial, RespuestaNino, Nino, PerfilCognitivo
from boom_api.permissions import EsPadre
from boom_api.serializers import EvaluacionInicialSerializer, RespuestaNinoSerializer


class EvaluacionInicialCreateView(generics.CreateAPIView):
    serializer_class = EvaluacionInicialSerializer
    permission_classes = (permissions.IsAuthenticated, EsPadre)

    def perform_create(self, serializer):
        nino = get_object_or_404(
            Nino, pk=self.request.data.get('nino_id'), padre__user=self.request.user
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

        perfil_cognitivo_sencillo = self.generar_perfil_cognitivo(evaluacion)

        PerfilCognitivo.objects.update_or_create(
            nino=evaluacion.nino,
            defaults={'resultado': perfil_cognitivo_sencillo}
        )

        return Response(self.get_serializer(evaluacion).data)

    #este perfil cognitivo es temporal faltara pulirse con datos historicos o con un profesional 
    def generar_perfil_cognitivo(self, evaluacion):
        respuestas = evaluacion.respuestas.all()

        puntajes = {}
        for r in respuestas:
            puntajes.setdefault(r.tipo, []).append(r.valor)

        resultado = {}
        for tipo, valores in puntajes.items():
            promedio = sum(valores) / len(valores)
            if promedio >= 7:
                nivel = "bajo apoyo"
            elif promedio >= 4:
                nivel = "apoyo moderado"
            else:
                nivel = "apoyo alto"
            resultado[tipo] = {"promedio": promedio, "nivel": nivel}
        return resultado