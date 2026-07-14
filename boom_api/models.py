from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"


class Profiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles")
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.first_name} {self.user.last_name}"


class Padre(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="padre")
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Padre"
        verbose_name_plural = "Padres"

    def __str__(self):
        return f"Padre: {self.user.first_name} {self.user.last_name}"


class Docente(models.Model):
    id_docente = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="docente")
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    curp = models.CharField(max_length=18, null=True, blank=True, unique=True)
    rfc = models.CharField(max_length=13, null=True, blank=True)
    campus = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    AreaEspecializada = models.CharField(max_length=100)
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"

    def __str__(self):
        return f"Docente:  {self.user.first_name} {self.user.last_name}"

class Terapeuta(models.Model):
    id_terapeuta = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="terapeuta")
    
    # Datos Personales
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='terapeutas/fotos/', blank=True, null=True)
    
    # Identificación Oficial y Fiscal (México)
    curp = models.CharField(max_length=18, null=True, blank=True, unique=True)
    rfc = models.CharField(max_length=13, null=True, blank=True) # Limitado a 13 caracteres para México
    regimen_fiscal = models.CharField(max_length=100, blank=True, null=True)

    # Datos Profesionales
    especialidad = models.CharField(max_length=100)
    enfoque = models.CharField(max_length=100, blank=True, null=True)
    institucion_egreso = models.CharField(max_length=150, blank=True, null=True)
    cedula_profesional = models.CharField(max_length=20, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    modalidad = models.CharField(max_length=50, blank=True, null=True) 
    idiomas = models.CharField(max_length=100, default="Español")
    estatus = models.CharField(max_length=50, default="Pendiente")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Terapeuta"
        verbose_name_plural = "Terapeutas"

    def __str__(self):
        return f"Terapeuta: {self.user.get_full_name()}"

class Nino(models.Model):
    id = models.BigAutoField(primary_key=True)
    nickname = models.CharField(max_length=50, unique=True)
    fecha_nacimiento = models.DateField()
    pin_acceso = models.CharField(max_length=128)  # se guarda hasheado, ver save()

    padre = models.ForeignKey(
        Padre, on_delete=models.CASCADE, related_name="ninos"
    )
    docente = models.ForeignKey(
        Docente, on_delete=models.SET_NULL, null=True, blank=True, related_name="alumnos"
    )

    terapeuta = models.ForeignKey(
        Terapeuta,on_delete=models.SET_NULL,null=True,blank=True, related_name="paciente"
    )

    nivel_apoyo = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatares_ninos/", blank=True, null=True)
    consentimiento_padre = models.BooleanField(
        default=False,
        help_text="Confirmación del padre/tutor para el tratamiento de datos del menor (LFPDPPP)."
    )
    activo = models.BooleanField(default=True)
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Niño"
        verbose_name_plural = "Niños"

    def __str__(self):
        return f"{self.nickname}"

    def set_pin(self, raw_pin):
        self.pin_acceso = make_password(raw_pin)

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.pin_acceso)

    def save(self, *args, **kwargs):
        if self.pin_acceso and not self.pin_acceso.startswith(
            ("pbkdf2_", "argon2", "bcrypt")
        ):
            self.pin_acceso = make_password(self.pin_acceso)
        super().save(*args, **kwargs)

class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="administrador")
    clave_admin = models.CharField(max_length=255,null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    fecha_nacimiento = models.DateField()
    GradoAcademico = models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return "Perfil del admin "+self.user.first_name+" "+self.user.last_name

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profiles.objects.create(user=instance)