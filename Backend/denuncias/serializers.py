from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Denuncia
from usuarios.serializers import UserSerializer
from comunicaciones.serializers import PosteoSerializer, EventoSerializer

class DenunciaSerializer(serializers.ModelSerializer):
    denunciante = UserSerializer(read_only=True)
    usuario_denunciado = UserSerializer(read_only=True)
    posteo_denunciado = PosteoSerializer(read_only=True)
    evento_denunciado = EventoSerializer(read_only=True)

    class Meta:
        model = Denuncia
        fields = [
            'id', 'denunciante', 'tipo',
            'usuario_denunciado', 'posteo_denunciado', 'evento_denunciado',
            'comentario', 'fecha_creacion', 'estado'
        ]
        read_only_fields = ['denunciante', 'fecha_creacion', 'estado']

class CrearDenunciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Denuncia
        fields = ['tipo', 'usuario_denunciado', 'posteo_denunciado', 
                 'evento_denunciado', 'comentario']

    def validate(self, data):
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError("Usuario no autenticado")

        try:
            denuncia = Denuncia(
                denunciante=request.user,
                **data
            )
            denuncia.clean()
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return data
