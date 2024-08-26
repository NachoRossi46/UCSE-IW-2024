from django.contrib import admin
from .models import Edificio, Departamento
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['idDuenio'].queryset = User.objects.exclude(rol__rol='Inquilino')

@admin.register(Edificio)
class EdificioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'numero')
    search_fields = ('nombre', 'direccion')


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    form = DepartamentoForm
    list_display = ('idEdificio', 'piso', 'numero', 'idDuenio', 'idOcupante', 'ocupaDepto')
    search_fields = ('idEdificio__nombre', 'piso', 'numero')
    list_filter = ('idEdificio__nombre', 'piso', 'ocupaDepto')
    raw_id_fields = ('idDuenio', 'idOcupante')
    autocomplete_fields = ['idDuenio', 'idOcupante']
    ordering = ('idEdificio', 'piso', 'numero')

    def get_readonly_fields(self, request, obj=None):
        # Evitar la edición de un departamento una vez creado
        if obj:
            return ['idEdificio']
        return []

    def has_add_permission(self, request):
        # Permitir solo a superusuarios agregar edificios y departamentos
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        # Permitir solo a superusuarios editar edificios y departamentos
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        # Permitir solo a superusuarios eliminar edificios y departamentos
        return request.user.is_superuser
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['idDuenio'].queryset = User.objects.exclude(rol__rol='Inquilino')
        return form
    




