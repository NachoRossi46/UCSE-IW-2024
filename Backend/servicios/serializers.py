from rest_framework import serializers
from .models import TipoServicio, Servicio
from propiedades.models import Edificio

class TipoServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServicio
        fields = ['id', 'tipo']

class ServicioSerializer(serializers.ModelSerializer):
    tipo = TipoServicioSerializer(read_only=True)
    tipo_id = serializers.PrimaryKeyRelatedField(queryset=TipoServicio.objects.all(), write_only=True, source='tipo')
    edificios = serializers.PrimaryKeyRelatedField(many=True, queryset=Edificio.objects.all())

    class Meta:
        model = Servicio
        fields = ['id', 'tipo', 'tipo_id', 'nombre_proveedor', 'telefono', 'edificios']

class ServicioEdificioSerializer(serializers.ModelSerializer):
    tipo = TipoServicioSerializer(read_only=True)

    class Meta:
        model = Servicio
        fields = ['id', 'tipo', 'nombre_proveedor', 'telefono']