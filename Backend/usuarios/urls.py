from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'usuarios', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('registro/', AuthViewSet.as_view({'post': 'registro'}), name='user-registro'),
    path('login/', AuthViewSet.as_view({'post': 'login'}), name='user-login'),
    path('logout/', AuthViewSet.as_view({'post': 'logout'}), name='user-logout'),
]

