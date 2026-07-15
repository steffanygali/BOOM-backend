from rest_framework.permissions import BasePermission


class EsPadre(BasePermission):
    message = "Solo un padre/tutor puede realizar esta acción."

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "padre")


class EsDocente(BasePermission):
    message = "Solo un docente puede realizar esta acción."

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "docente")


class EsTerapeuta(BasePermission):
    message = "Solo un terapeuta puede realizar esta acción."

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "terapeuta")


class EsDocenteOTerapeuta(BasePermission):
    message = "Solo personal educativo (docente o terapeuta) puede realizar esta acción."

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (hasattr(user, "docente") or hasattr(user, "terapeuta"))


class EsAdministrador(BasePermission):
    message = "Solo un administrador puede realizar esta acción."

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "administrador")


# --- Permisos a nivel de objeto (sobre un Nino específico) -----------------

class EsPadreDelNino(BasePermission):
    message = "No tienes acceso a este niño."

    def has_object_permission(self, request, view, obj):
        return hasattr(request.user, "padre") and obj.padre_id == request.user.padre.id


class EsEducadorAsignadoAlNino(BasePermission):
    message = "No tienes a este niño asignado."

    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(user, "docente") and obj.docente_id == user.docente.id_docente:
            return True
        if hasattr(user, "terapeuta") and obj.terapeuta_id == user.terapeuta.id_terapeuta:
            return True
        return False