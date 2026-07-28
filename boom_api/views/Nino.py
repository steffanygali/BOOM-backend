import random
import string
from django.db.models import *
from django.db import transaction
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


def generar_pin(largo=6):
    return ''.join(random.choices(string.digits, k=largo))


class NinoCreateView(generics.CreateAPIView):
    serializer_class = NinoCreateSerializer
    permission_classes = (permissions.IsAuthenticated, EsPadre)

    @extend_schema(
        summary="Registrar un niño (para padre de familia)",
        description="Endpoint para que un padre autenticado registre un nuevo niño/a. Si no se envía pin_acceso, se genera uno de 6 dígitos automáticamente.",
        tags=["Niño"],
        responses={
            201: dict(description="Niño registrado exitosamente", example={"id": 1, "nickname": "Carlitos", "fecha_nacimiento": "2018-05-10", "pin_generado": "123456"}),
            400: dict(description="Error de validación o nickname duplicado"),
            403: dict(description="Solo un padre/tutor puede registrar niños")
        }
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        pin_generado = None
        if not data.get('pin_acceso'):
            pin_generado = generar_pin()
            data['pin_acceso'] = pin_generado

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        # padre se asigna aquí, nunca desde el request
        nino = serializer.save(padre=request.user.padre)

        response_data = serializer.data
        if pin_generado:
            # única vez que se expone el PIN en texto plano
            response_data['pin_generado'] = pin_generado
        return Response(response_data, status=status.HTTP_201_CREATED)
