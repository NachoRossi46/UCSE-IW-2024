from rest_framework import serializers
from .models import Edificio
from usuarios.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nombre', 'apellido']

class EdificioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edificio
        fields = ['id', 'nombre', 'direccion', 'numero', 'ciudad']

class EdificioDetailSerializer(serializers.ModelSerializer):
    usuarios = UserSerializer(many=True, read_only=True, source='usuarios.all')
    cantidad_servicios = serializers.SerializerMethodField()

    class Meta:
        model = Edificio
        fields = ['id', 'nombre', 'direccion', 'numero', 'ciudad', 'usuarios', 'cantidad_servicios']

    def get_cantidad_servicios(self, obj):
        return obj.servicios.count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Agregar información básica de servicios si se requiere
        if self.context.get('include_services', False):
            from servicios.serializers import ServicioListSerializer
            servicios = instance.servicios.all()
            representation['servicios'] = ServicioListSerializer(servicios, many=True).data
        return representation



