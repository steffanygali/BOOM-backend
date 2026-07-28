from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, inline_serializer

from boom_api.models import Profiles

ROLES_ATTR = ["padre", "docente", "terapeuta", "administrador"]


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if not user.is_active:
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        role_names = [rol for rol in ROLES_ATTR if hasattr(user, rol)]

        # Invalida cualquier token anterior (otros dispositivos) y crea uno nuevo
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)

        return Response({
            'id': user.pk,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'token': token.key,
            'roles': role_names
        })


class Logout(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response({'logout': True})


class UserMeView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        summary="Obtener datos del usuario autenticado",
        description="Devuelve el perfil del usuario autenticado (id, first_name, last_name, email, rol) y si es padre, la lista de sus niños.",
        tags=["Autenticación"],
        responses={
            200: inline_serializer(
                name="UserMeResponse",
                fields={
                    "id": serializers.IntegerField(),
                    "first_name": serializers.CharField(),
                    "last_name": serializers.CharField(),
                    "email": serializers.EmailField(),
                    "rol": serializers.CharField(help_text="Rol del usuario: padre, docente, terapeuta, admin"),
                    "ninos": serializers.ListField(
                        child=serializers.DictField(),
                        required=False,
                        help_text="Lista de niños asociados al padre"
                    )
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        rol = "desconocido"
        if hasattr(user, "padre"):
            rol = "padre"
        elif hasattr(user, "docente"):
            rol = "docente"
        elif hasattr(user, "terapeuta"):
            rol = "terapeuta"
        elif hasattr(user, "administrador") or user.is_superuser or user.is_staff:
            rol = "admin"

        data = {
            "id": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "rol": rol
        }

        if rol == "padre":
            ninos = user.padre.ninos.filter(activo=True)
            data["ninos"] = [
                {
                    "id": n.id,
                    "nickname": n.nickname,
                    "fecha_nacimiento": str(n.fecha_nacimiento),
                    "nivel_apoyo": n.nivel_apoyo,
                    "activo": n.activo,
                }
                for n in ninos
            ]

        return Response(data, status=status.HTTP_200_OK)

    