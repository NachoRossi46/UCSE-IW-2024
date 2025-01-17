from django.contrib import admin
from .models import Conversacion, Mensaje

class MensajeInline(admin.TabularInline):
    model = Mensaje
    readonly_fields = ('fecha_envio',)
    extra = 0
    can_delete = True
    fields = ('remitente', 'contenido', 'fecha_envio', 'leido')

@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_participantes', 'get_edificio', 'fecha_creacion', 'ultima_actualizacion', 'get_mensajes_count')
    list_filter = ('fecha_creacion', 'ultima_actualizacion')
    search_fields = ('participantes__email', 'participantes__nombre', 'participantes__apellido')
    date_hierarchy = 'fecha_creacion'
    inlines = [MensajeInline]
    readonly_fields = ('fecha_creacion', 'ultima_actualizacion')
    
    def get_participantes(self, obj):
        return ", ".join([f"{user.nombre} {user.apellido}" for user in obj.participantes.all()])
    get_participantes.short_description = "Participantes"

    def get_edificio(self, obj):
        # Obtenemos el edificio del primer participante (todos deberían ser del mismo edificio)
        participante = obj.participantes.first()
        return participante.edificio.nombre if participante and participante.edificio else "Sin edificio"
    get_edificio.short_description = "Edificio"

    def get_mensajes_count(self, obj):
        return obj.mensajes.count()
    get_mensajes_count.short_description = "Cantidad de mensajes"

@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_conversacion_id', 'remitente', 'contenido_truncado', 'fecha_envio', 'leido')
    list_filter = ('fecha_envio', 'leido', 'remitente__edificio')
    search_fields = ('contenido', 'remitente__email', 'remitente__nombre', 'remitente__apellido')
    date_hierarchy = 'fecha_envio'
    readonly_fields = ('fecha_envio',)
    raw_id_fields = ('conversacion', 'remitente')
    
    def contenido_truncado(self, obj):
        return obj.contenido[:50] + '...' if len(obj.contenido) > 50 else obj.contenido
    contenido_truncado.short_description = "Contenido"

    def get_conversacion_id(self, obj):
        return f"Conversación #{obj.conversacion.id}"
    get_conversacion_id.short_description = "Conversación"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('remitente', 'conversacion')
