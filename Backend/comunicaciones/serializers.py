from rest_framework import serializers
from .models import Posteo, TipoPosteo
from usuarios.models import User
from django.utils import timezone
from django.utils.formats import date_format

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nombre', 'apellido', 'piso', 'numero']


class TipoPosteoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPosteo
        fields = ['id', 'tipo']

class PosteoSerializer(serializers.ModelSerializer):
    tipo_posteo = TipoPosteoSerializer(read_only=True)
    tipo_posteo_id = serializers.PrimaryKeyRelatedField(queryset=TipoPosteo.objects.all(), source='tipo_posteo', write_only=True)
    usuario = UserDetailSerializer(read_only=True)
    fecha_creacion_legible = serializers.SerializerMethodField()


    class Meta:
        model = Posteo
        fields = ['id', 'titulo', 'descripcion', 'usuario', 'tipo_posteo', 'tipo_posteo_id', 'imagen', 'fecha_creacion_legible']
        read_only_fields = ['usuario', 'fecha_creacion_legible']

    def get_fecha_creacion_legible(self, obj):
        return date_format(timezone.localtime(obj.fecha_creacion), format="DATETIME_FORMAT")

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)
