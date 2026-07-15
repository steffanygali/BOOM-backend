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
from boom_api.serializers_docs import RegistroTerapeutaInputSerializer

class TerapeutaViews(generics.CreateAPIView):

    permission_classes = (EsAdministrador,)

    @extend_schema(
        request=RegistroTerapeutaInputSerializer,
        summary="Registrar un nuevo Terapeuta",
        description="Crea un usuario administrador secundario e indexa su perfil clínico, fiscal y académico.",
        responses={
            201: dict(description="Terapeuta registrado con éxito", example={"Terapeuta registrado": 1}),
            400: dict(description="Error de validación, CURP, RFC o correo duplicados")
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

            especialidad = request.data.get('especialidad')
            if not especialidad:
                return Response({"message": "especialidad es requerida"}, status=400)

            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                return Response({"message": "Nombre de usuario " + email + ", ya existe"}, 400)

            user = User.objects.create(username=email, email=email,
                                        first_name=first_name, last_name=last_name,
                                        is_active=1)
            user.save()
            user.set_password(password)
            user.save()

            terapeuta = Terapeuta.objects.create(
                user=user,
                fecha_nacimiento=request.data['fecha_nacimiento'],
                telefono=request.data.get('telefono'),
                direccion=request.data.get('direccion'),
                curp=request.data.get('curp'),
                rfc=request.data.get('rfc'),
                regimen_fiscal=request.data.get('regimen_fiscal'),
                especialidad=especialidad,
                enfoque=request.data.get('enfoque'),
                institucion_egreso=request.data.get('institucion_egreso'),
                cedula_profesional=request.data.get('cedula_profesional'),
                biografia=request.data.get('biografia'),
                modalidad=request.data.get('modalidad'),
                idiomas=request.data.get('idiomas', 'Español'),
            )

            return Response({"Terapeuta registrado": terapeuta.id_terapeuta}, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
