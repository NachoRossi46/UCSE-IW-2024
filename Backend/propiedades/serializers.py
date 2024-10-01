from rest_framework import serializers
from .models import Edificio
from usuarios.models import User
from servicios.serializers import ServicioEdificioSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nombre', 'apellido']

class EdificioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edificio
        fields = ['id', 'nombre', 'direccion', 'numero', 'ciudad']

class EdificioDetailSerializer(serializers.ModelSerializer):
    usuarios = UserSerializer(many=True, read_only=True)
    servicios = ServicioEdificioSerializer(many=True, read_only=True)

    class Meta:
        model = Edificio
        fields = ['id', 'nombre', 'direccion', 'numero', 'ciudad', 'usuarios', 'servicios']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        usuarios = User.objects.filter(edificio=instance)
        representation['usuarios'] = UserSerializer(usuarios, many=True).data
        return representation


