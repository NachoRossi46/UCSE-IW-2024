from django.contrib import admin
from .models import TipoServicio, Servicio

@admin.register(TipoServicio)
class TipoServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo')
    search_fields = ('tipo',)

class ServicioEdificioInline(admin.TabularInline):
    model = Servicio.edificios.through
    extra = 1

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'nombre_proveedor', 'telefono')
    list_filter = ('tipo',)
    search_fields = ('nombre_proveedor', 'telefono')
    filter_horizontal = ('edificios',)
    inlines = [ServicioEdificioInline]
    fieldsets = (
        (None, {
            'fields': ('tipo', 'nombre_proveedor', 'telefono')
        }),
        ('Edificios', {
            'fields': ('edificios',),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('edificios')