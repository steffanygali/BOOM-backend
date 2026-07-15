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
from boom_api.serializers_docs import RegistroAdminInputSerializer

class AdminViews(generics.CreateAPIView):

    permission_classes = (EsAdministrador,)

    @extend_schema(
        request=RegistroAdminInputSerializer,
        summary="Registrar un nuevo Administrador",
        description="Permite dar de alta cuentas administrativas adicionales con accesos totales globales.",
        responses={
            201: dict(description="Administrador registrado con éxito", example={"Administrador registrado": 2}),
            400: dict(description="Error de validación o correo duplicado")
        },
        tags=["Registro"]
    )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)

        if user.is_valid():
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data.get('password')
            if not password:
                return Response({"message": "La contraseña es requerida"}, status=400)

            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                return Response({"message": "Nombre de usuario " + email + ", ya existe"}, 400)

            user = User.objects.create(username=email, email=email,
                                        first_name=first_name, last_name=last_name,
                                        is_active=1)
            user.save()
            user.set_password(password)
            user.save()

            admin = Administradores.objects.create(
                user=user,
                fecha_nacimiento=request.data['fecha_nacimiento'],
                clave_admin=request.data.get('clave_admin'),
                telefono=request.data.get('telefono'),
                rfc=request.data.get('rfc'),
                GradoAcademico=request.data.get('GradoAcademico'),
            )

            return Response({"Administrador registrado": admin.id}, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)