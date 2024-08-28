from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Rol

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'nombre', 'apellido', 'rol', 'edificio', 'piso', 'numero', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active', 'rol', 'edificio', 'piso', 'numero')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('nombre', 'apellido', 'rol', 'edificio')}),
        ('Permisos', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'apellido', 'rol', 'edificio', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'nombre', 'apellido')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Rol)

