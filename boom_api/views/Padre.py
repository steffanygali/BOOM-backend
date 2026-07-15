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
from boom_api.serializers_docs import RegistroPadreInputSerializer
class PadreViews(generics.CreateAPIView):

    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        request=RegistroPadreInputSerializer,
        summary="Registrar un nuevo Padre de Familia",
        description="Endpoint público para que los padres de familia creen su cuenta en la plataforma.",
        responses={
            201: dict(description="Padre registrado con éxito", example={"Padre registrado": 1}),
            400: dict(description="Error de validación o correo duplicado")
        },
        tags=["Registro"]
    )
    @transaction.atomic
    def post(self, request, *args, **kwargs):

        user = UserSerializer(data= request.data)

        if  user.is_valid():
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data.get('password')
            if not password:
                return Response({"message": "La contraseña es requerida"}, status=400)

            # prueva si es que existe las url de si es que existe 
            existing_user = User.objects.filter(email=email).first()

            if existing_user:
                return Response({"message":"Nombre de usuario "+email+", ya existe"},400)

            user = User.objects.create( username = email,
                                        email = email,
                                        first_name = first_name,
                                        last_name = last_name,
                                        is_active = 1)

            user.save()
            user.set_password(password)
            user.save()

            #Alamacenar los demas datos del padre 
            padre = Padre.objects.create(
                user=user,
                fecha_nacimiento=request.data['fecha_nacimiento'],
                telefono=request.data['telefono'],
                direccion=request.data['direccion'],
            )

            padre.save()

            return Response({"Padre registrado": padre.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
