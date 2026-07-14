from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

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
    