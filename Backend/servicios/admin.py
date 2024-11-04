from django.contrib import admin
from .models import TipoServicio, Servicio
from django.utils.html import format_html

@admin.register(TipoServicio)
class TipoServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo')
    search_fields = ('tipo',)
    ordering = ('tipo',)

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'nombre_proveedor', 'telefono', 'edificio_display', 'fecha_creacion')
    list_filter = ('tipo', 'edificio', 'fecha_creacion')
    search_fields = ('nombre_proveedor', 'telefono', 'edificio__nombre')
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

    fieldsets = (
        (None, {
            'fields': ('tipo', 'nombre_proveedor', 'telefono', 'edificio')
        }),
        ('Información Temporal', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',),
        }),
    )

    def edificio_display(self, obj):
        if obj.edificio:
            return format_html(
                '<span style="color: #1e88e5;">{}</span>',
                obj.edificio.nombre
            )
        return format_html(
            '<span style="color: #e57373;">Sin edificio asignado</span>'
        )
    edificio_display.short_description = 'Edificio'
    edificio_display.admin_order_field = 'edificio__nombre'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('edificio', 'tipo')

    def get_search_results(self, request, queryset, search_term):
        # Mejora la búsqueda para incluir el edificio
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        
        if search_term:
            queryset |= self.model.objects.filter(
                edificio__nombre__icontains=search_term
            ).distinct()
        
        return queryset, use_distinct
