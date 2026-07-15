from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.bootstrap import VersionView
from boom_api.views.auth import CustomAuthToken ,Logout
from boom_api.views.Admin import *
from boom_api.views.Docente import *
from boom_api.views.Padre import *
from boom_api.views.Terapeuta import *

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)



urlpatterns = [
    path("api/version/", VersionView.as_view()),
    path('api/login/', CustomAuthToken.as_view()),
    path('api/logout/', Logout.as_view()),
    
    #apis para los registros 
    path("api/register/administrador/", AdminViews.as_view()),
    path("api/register/docente/",DocenteViews.as_view()),
    path("api/register/padre/", PadreViews.as_view()),
    path("api/register/terapeuta/", TerapeutaViews.as_view()),


    #endpoints de documentacion

    # ====== ENDPOINTS DE LA DOCUMENTACIÓN ======
    # Genera el archivo plano de configuración (OpenAPI Schema)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Interfaz Interactiva Web (Swagger UI) 
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Interfaz Técnica limpia alternativa (Redoc)
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
