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
