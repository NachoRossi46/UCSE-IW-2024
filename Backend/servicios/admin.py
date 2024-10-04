from django.contrib import admin
from .models import TipoServicio, Servicio
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

@admin.register(TipoServicio)
class TipoServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo')
    search_fields = ('tipo',)

class ServicioEdificioInline(admin.TabularInline):
    model = Servicio.edificios.through
    extra = 1

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'nombre_proveedor', 'telefono', 'edificio_display')
    list_filter = ('tipo','edificios')
    search_fields = ('nombre_proveedor', 'telefono','edificio__nombre')
    filter_horizontal = ('edificios',)
    inlines = [ServicioEdificioInline]

    fieldsets = (
        (None, {
            'fields': ('tipo', 'nombre_proveedor', 'telefono')
        }),
        ('Edificios Asociados', {
            'fields': ('edificios',),
            'classes': ('collapse',),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('edificios')

    def edificio_display(self, obj):
        return format_html_join(mark_safe(' - '),'{}',((edificio.nombre,) for edificio in obj.edificios.all())) or "Sin edificios" 
    edificio_display.short_description = 'Edificios'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if 'edificios' in form.changed_data:
            obj.edificios.set(form.cleaned_data['edificios'])
