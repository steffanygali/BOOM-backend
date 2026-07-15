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
from boom_api.serializers_docs import RegistroDocenteInputSerializer

class DocenteViews(generics.CreateAPIView):

    permission_classes = (EsAdministrador,)

    @extend_schema(
        request=RegistroDocenteInputSerializer,
        summary="Registrar un nuevo Docente",
        description="Crea un usuario del sistema y añade su perfil detallado con CURP, RFC y Campus académico.",
        responses={
            201: dict(description="Docente registrado con éxito", example={"Docente registrado": 1}),
            400: dict(description="Error de validación, CURP o correo duplicados")
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

            campus = request.data.get('campus')
            area_especializada = request.data.get('AreaEspecializada')
            curp_data = request.data.get('curp')
            rfc_data = request.data.get('rfc')

            if not campus or not area_especializada:
                return Response(
                    {"message": "campus y AreaEspecializada son requeridos"}, status=400
                )

            # 1. Validar si el usuario (email) ya existe
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                return Response({"message": "Nombre de usuario " + email + ", ya existe"}, 400)

            # 2. Validar CURP en el modelo Docente (No en User)
            if curp_data:
                if Docente.objects.filter(curp=curp_data).exists():
                    return Response({"message": "El CURP ya está registrado por otro docente."}, status=400)

            # 3. Validar RFC en el modelo Docente (Opcional, por seguridad)
            if rfc_data:
                if Docente.objects.filter(rfc=rfc_data).exists():
                    return Response({"message": "El RFC ya está registrado por otro docente."}, status=400)

            # Si pasa todas las validaciones, creamos el usuario
            user = User.objects.create(username=email, email=email,
                                        first_name=first_name, last_name=last_name,
                                        is_active=1)
            user.save()
            user.set_password(password)
            user.save()

            docente = Docente.objects.create(
                user=user,
                fecha_nacimiento=request.data['fecha_nacimiento'],
                telefono=request.data.get('telefono'),
                direccion=request.data.get('direccion'),
                curp=curp_data,
                rfc=rfc_data,
                campus=campus,
                AreaEspecializada=area_especializada,
            )

            return Response({"Docente registrado": docente.id_docente}, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
