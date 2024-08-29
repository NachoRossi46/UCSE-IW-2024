from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PosteoViewSet, TipoPosteoListView

router = DefaultRouter()
router.register(r'posteos', PosteoViewSet, basename='posteo')

urlpatterns = [
    path('', include(router.urls)),
    path('tipos-posteo/', TipoPosteoListView.as_view(), name='tipo-posteo-list'),
]
