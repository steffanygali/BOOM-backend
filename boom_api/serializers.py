from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

#Serealizaciones de nuestras app 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")

class ProfilesSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profiles
        fields = "__all__"

class PadreSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Padre
        fields = "__all__"

class DocenteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Docente
        fields = "__all__"

class TerapeutaSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Terapeuta
        fields = "__all__"

class NinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nino
        fields = [
            "id", "nickname", "fecha_nacimiento", "padre", "docente", "terapeuta",
            "nivel_apoyo", "avatar", "consentimiento_padre", "activo",
            "creation", "update",
        ]


class NinoCreateSerializer(serializers.ModelSerializer):
    pin_acceso = serializers.CharField(write_only=True, min_length=4, max_length=12)

    class Meta:
        model = Nino
        fields = [
            "id", "nickname", "fecha_nacimiento", "padre", "docente", "terapeuta",
            "nivel_apoyo", "avatar", "consentimiento_padre", "pin_acceso",
        ]

class AdministradoresSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = "__all__"