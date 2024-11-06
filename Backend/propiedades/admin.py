from django.contrib import admin
from django.core.exceptions import PermissionDenied
from .models import Edificio
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(Edificio)
class EdificioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'numero', 'ciudad')
    list_filter = ('ciudad',)
    search_fields = ('nombre', 'direccion', 'ciudad')
    
    fieldsets = (
        ('Información del Edificio', {
            'fields': ('nombre', 'direccion', 'numero', 'ciudad')
        }),
    )
    
    def has_add_permission(self, request):
        # Solo permitir agregar si es superusuario o tiene rol Administrador
        return request.user.is_superuser or request.user.rol.rol == 'Administrador'
    
    def has_change_permission(self, request, obj=None):
        # Solo permitir modificar si es superusuario o tiene rol Administrador
        return request.user.is_superuser or request.user.rol.rol == 'Administrador'
    
    def has_delete_permission(self, request, obj=None):
        # Solo permitir eliminar si es superusuario o tiene rol Administrador
        return request.user.is_superuser or request.user.rol.rol == 'Administrador'