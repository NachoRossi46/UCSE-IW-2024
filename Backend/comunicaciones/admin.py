from django.contrib import admin
from .models import Posteo, TipoPosteo, Respuesta, TipoEvento, Evento

@admin.register(TipoPosteo)
class TipoPosteoAdmin(admin.ModelAdmin):
    list_display = ['tipo']
    
@admin.register(TipoEvento)
class TipoEventoAdmin(admin.ModelAdmin):
    list_display = ['tipo']    
    
class RespuestaInline(admin.StackedInline):
    model = Respuesta
    extra = 0
    readonly_fields = ['fecha_creacion']


@admin.register(Posteo)
class PosteoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'tipo_posteo', 'fecha_creacion', 'respuestas_count']
    list_filter = ['tipo_posteo', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'usuario__email']
    inlines = [RespuestaInline]
    
    def respuestas_count(self, obj):
        return obj.respuestas.count()
    respuestas_count.short_description = 'Número de respuestas'

@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ['posteo', 'usuario', 'contenido_truncado', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['contenido', 'usuario__email', 'posteo__titulo']
    readonly_fields = ['fecha_creacion']

    def contenido_truncado(self, obj):
        return obj.contenido[:50] + '...' if len(obj.contenido) > 50 else obj.contenido
    contenido_truncado.short_description = 'Contenido'
    
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'tipo_evento', 'fecha_inicio', 'fecha_fin']
    list_filter = ['tipo_evento', 'fecha_inicio', 'fecha_fin']
    search_fields = ['titulo', 'descripcion', 'usuario__email']

    fieldsets = (
        (None, {
            'fields': ('titulo', 'descripcion', 'usuario', 'tipo_evento')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

