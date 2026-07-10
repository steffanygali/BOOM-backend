from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.bootstrap import VersionView
from boom_api.views.auth import CustomAuthToken ,Logout

urlpatterns = [
    path("api/version/", VersionView.as_view()),
    path('api/login/', CustomAuthToken.as_view()),
    path('api/logout/', Logout.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
