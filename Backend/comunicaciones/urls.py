from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PosteoViewSet, TipoPosteoListView, RespuestaViewSet, EventoViewSet, PosteoSearchViewSet, rebuild_index

router = DefaultRouter()
router.register(r'posteos', PosteoViewSet, basename='posteo')
router.register(r'eventos', EventoViewSet, basename='evento')
router.register(r'search', PosteoSearchViewSet, basename='posteo-search')

urlpatterns = [
    path('', include(router.urls)),
    path('tipos-posteo/', TipoPosteoListView.as_view(), name='tipo-posteo-list'),
    path('posteos/<int:posteo_pk>/respuestas/', RespuestaViewSet.as_view({'get': 'list', 'post': 'create'}), name='respuesta-list'),
    path('posteos/<int:posteo_pk>/respuestas/<int:pk>/', RespuestaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='respuesta-detail'),

]
