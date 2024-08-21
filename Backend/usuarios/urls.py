from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AuthViewSet

from django.contrib.auth import views as auth_views
from . import views

router = DefaultRouter()
router.register(r'usuarios', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('dashboard/', views.dashboard, name='dashboard'),
    #path('registro/', views.registro, name='registro'),
    #path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('registro/', AuthViewSet.as_view({'post': 'registro'}), name='user-registro'),
    path('login/', AuthViewSet.as_view({'post': 'login'}), name='user-login'),
    path('logout/', AuthViewSet.as_view({'post': 'logout'}), name='user-logout'),
]

"""
path('registro/', AuthViewSet.as_view({'post': 'registro'}), name='user-registro'),
path('login/', AuthViewSet.as_view({'post': 'login'}), name='user-login'),
path('logout/', AuthViewSet.as_view({'post': 'logout'}), name='user-logout'),
"""