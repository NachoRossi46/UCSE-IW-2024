from django.contrib import admin
from .models import Posteo, TipoPosteo

@admin.register(TipoPosteo)
class TipoPosteoAdmin(admin.ModelAdmin):
    list_display = ['tipo']

@admin.register(Posteo)
class PosteoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'tipo_posteo', 'fecha_creacion']
    list_filter = ['tipo_posteo', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'usuario__email']

