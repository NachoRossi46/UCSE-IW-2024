from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipoServicioViewSet, ServicioViewSet

router = DefaultRouter()
router.register(r'tipos', TipoServicioViewSet)
router.register(r'', ServicioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

