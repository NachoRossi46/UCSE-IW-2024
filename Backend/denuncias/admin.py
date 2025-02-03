from django.contrib import admin
from .models import Denuncia

@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'get_contenido_denunciado', 'denunciante',
                   'fecha_creacion', 'estado')
    list_filter = ('tipo', 'estado', 'fecha_creacion')
    search_fields = ('denunciante__email', 'comentario', 
                    'usuario_denunciado__email',
                    'posteo_denunciado__titulo',
                    'evento_denunciado__titulo')
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ('fecha_creacion',)
