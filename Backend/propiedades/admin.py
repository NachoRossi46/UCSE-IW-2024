from django.contrib import admin
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








