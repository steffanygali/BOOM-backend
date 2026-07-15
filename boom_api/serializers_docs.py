# boom_api/serializers_docs.py
from rest_framework import serializers

class RegistroPadreInputSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150, help_text="Nombre(s) del padre o tutor")
    last_name = serializers.CharField(max_length=150, help_text="Apellidos del padre o tutor")
    email = serializers.EmailField(help_text="Correo electrónico (se usará como nombre de usuario)")
    password = serializers.CharField(write_only=True, min_length=8, help_text="Contraseña segura")
    fecha_nacimiento = serializers.DateField(help_text="Formato: AAAA-MM-DD")
    telefono = serializers.CharField(max_length=20, required=False, help_text="Teléfono de contacto de 10 dígitos")
    direccion = serializers.CharField(max_length=255, required=False, help_text="Dirección residencial completa")


class RegistroDocenteInputSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    fecha_nacimiento = serializers.DateField()
    telefono = serializers.CharField(max_length=20, required=False)
    direccion = serializers.CharField(max_length=255, required=False)
    curp = serializers.CharField(max_length=18, min_length=18, help_text="Clave Única de Registro de Población (18 caracteres)")
    rfc = serializers.CharField(max_length=13, required=False, help_text="Registro Federal de Contribuyentes (13 caracteres)")
    campus = serializers.CharField(max_length=100, help_text="Campus al que pertenece el docente")
    AreaEspecializada = serializers.CharField(max_length=100, help_text="Área de especialización docente")


class RegistroTerapeutaInputSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    fecha_nacimiento = serializers.DateField()
    telefono = serializers.CharField(max_length=20, required=False)
    direccion = serializers.CharField(max_length=255, required=False)
    curp = serializers.CharField(max_length=18)
    rfc = serializers.CharField(max_length=13, required=False)
    regimen_fiscal = serializers.CharField(max_length=100, required=False, help_text="Ejemplo: RESICO, Sueldos y Salarios")
    especialidad = serializers.CharField(max_length=150)
    enfoque = serializers.CharField(max_length=150, required=False)
    institucion_egreso = serializers.CharField(max_length=150, required=False)
    cedula_profesional = serializers.CharField(max_length=20, required=False)
    biografia = serializers.CharField(required=False)
    modalidad = serializers.CharField(max_length=50, required=False, help_text="Ejemplo: Presencial, En línea, Híbrido")
    idiomas = serializers.CharField(max_length=100, required=False, help_text="Idiomas que domina, separados por comas")

class RegistroAdminInputSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    fecha_nacimiento = serializers.DateField()
    clave_admin = serializers.CharField(max_length=50, help_text="Clave interna única del administrador")
    telefono = serializers.CharField(max_length=20, required=False)
    rfc = serializers.CharField(max_length=13, required=False)
    GradoAcademico = serializers.CharField(max_length=100, required=False, help_text="Ejemplo: Licenciatura, Maestría")