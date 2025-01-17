from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from comunicaciones.views import robots_txt, rebuild_index
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('usuarios.urls')),
    path('propiedades/', include('propiedades.urls')),
    path('comunicaciones/', include('comunicaciones.urls')),
    path('servicios/', include('servicios.urls')),
    path('mensajeria/', include('mensajeria.urls')),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('rebuild_index/', rebuild_index, name='rebuild_index'),
    # URLs para la documentación
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


