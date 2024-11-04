from rest_framework import serializers
from .models import TipoServicio, Servicio

class TipoServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServicio
        fields = ['id', 'tipo']

class ServicioSerializer(serializers.ModelSerializer):
    tipo = TipoServicioSerializer(read_only=True)
    tipo_id = serializers.PrimaryKeyRelatedField(queryset=TipoServicio.objects.all(), write_only=True, source='tipo')
    edificio = serializers.PrimaryKeyRelatedField(read_only=True)
    fecha_creacion = serializers.DateTimeField(read_only=True)
    fecha_actualizacion = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Servicio
        fields = ['id', 'tipo', 'tipo_id', 'nombre_proveedor', 'telefono', 'edificio', 'fecha_creacion', 'fecha_actualizacion']
        
    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.user.rol.rol == 'Colaborador':
            if not request.user.edificio:
                raise serializers.ValidationError(
                    "El colaborador debe estar asignado a un edificio para crear servicios."
                )
        return attrs

class ServicioListSerializer(serializers.ModelSerializer):
    tipo = TipoServicioSerializer(read_only=True)

    class Meta:
        model = Servicio
        fields = ['id', 'tipo', 'nombre_proveedor', 'telefono']
