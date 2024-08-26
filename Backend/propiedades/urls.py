from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EdificioViewSet, DepartamentoViewSet

router = DefaultRouter()
router.register(r'edificios', EdificioViewSet)
router.register(r'departamentos', DepartamentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
