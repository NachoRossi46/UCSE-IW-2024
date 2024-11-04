from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipoServicioViewSet, ServicioViewSet

router = DefaultRouter()
router.register(r'tipos', TipoServicioViewSet, basename='tipo-servicio')
router.register(r'', ServicioViewSet, basename='servicio')

urlpatterns = [
    path('', include(router.urls)),
]

