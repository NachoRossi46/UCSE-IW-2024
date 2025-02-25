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
    path('request-password-reset/', AuthViewSet.as_view({'post': 'request_password_reset'}), name='request-password-reset'),
    path('reset-password/', AuthViewSet.as_view({'post': 'reset_password'}), name='reset-password'),
]