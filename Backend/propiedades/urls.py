from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EdificioViewSet

router = DefaultRouter()
router.register(r'edificios', EdificioViewSet, basename='edificio')

urlpatterns = [
    path('', include(router.urls)),
]
