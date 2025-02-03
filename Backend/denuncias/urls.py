from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DenunciaViewSet

# Crear router y registrar viewsets
router = DefaultRouter()
router.register(r'denuncias', DenunciaViewSet, basename='denuncia')

urlpatterns = [
    path('', include(router.urls)),
]
