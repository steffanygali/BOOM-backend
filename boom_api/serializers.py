from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

# Serializaciones de nuestra app

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
    pin_acceso = serializers.CharField(write_only=True, required=False, min_length=4, max_length=12)
    class Meta:
        model = Nino
        fields = [
            "id", "nickname", "fecha_nacimiento", "docente", "terapeuta",
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


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ["id", "titulo", "tipo", "nivel_dificultad", "instrucciones", "audio", "imagen", "activo"]


class RespuestaNinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaNino
        fields = ["id", "pregunta_texto", "tipo", "valor"]

class EvaluacionInicialSerializer(serializers.ModelSerializer):
    respuestas = RespuestaNinoSerializer(many=True, read_only=True)

    class Meta:
        model = EvaluacionInicial
        fields = ["id", "nino", "padre", "fecha_inicio", "fecha_fin", "completada", "respuestas"]
        read_only_fields = ["nino", "padre"]

class RegistroActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroActividad
        fields = ["id", "actividad", "tiempo_segundos", "completada"]


class SesionNinoSerializer(serializers.ModelSerializer):
    registros = RegistroActividadSerializer(many=True, read_only=True)

    class Meta:
        model = SesionNino
        fields = [
            "id", "nino", "padre", "inicio", "fin",
            "actividades_completadas", "tiempo_total_segundos", "registros",
        ]
        read_only_fields = ["nino", "padre", "actividades_completadas", "tiempo_total_segundos"]