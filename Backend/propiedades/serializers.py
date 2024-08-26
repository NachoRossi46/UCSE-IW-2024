from rest_framework import serializers
from .models import Edificio, Departamento
from usuarios.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nombre', 'apellido']

class EdificioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edificio
        fields = ['id', 'nombre']

class DepartamentoSerializer(serializers.ModelSerializer):
    duenio_info = UserSerializer(source='idDuenio', read_only=True)
    ocupante_info = UserSerializer(source='idOcupante', read_only=True)
    edificio_info = EdificioSerializer(source='idEdificio', read_only=True)
    
    class Meta:
        model = Departamento
        fields = ['id', 'edificio_info', 'piso', 'numero', 'duenio_info', 'ocupante_info', 'ocupaDepto']

    def validate(self, data):

        data['numero'] = data['numero'].upper()

        if Departamento.objects.filter(idEdificio=data['idEdificio'], numero=data['numero']).exists():
            raise serializers.ValidationError(f"Ya existe un departamento con el número {data['numero']} en el edificio seleccionado.")
        
        # validaciones adicionales si es necesario
        if data.get('idDuenio') and data.get('idOcupante') and data['idDuenio'] != data['idOcupante'] and data['ocupaDepto']:
            raise serializers.ValidationError("El campo 'ocupaDepto' debe estar en False si el dueño y el ocupante no son la misma persona.")
        if not data.get('idDuenio') and data.get('idOcupante'):
            raise serializers.ValidationError("Debe asignarse un dueño antes de asignar un ocupante.")
        if data.get('idOcupante') and not data['ocupaDepto']:
            raise serializers.ValidationError("El ocupante debe estar viviendo en el departamento, 'ocupaDepto' debe ser True.")
        return data
