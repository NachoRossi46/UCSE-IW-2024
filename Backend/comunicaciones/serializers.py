from rest_framework import serializers
from .models import Posteo, TipoPosteo, Respuesta, TipoEvento, Evento
from usuarios.models import User
from django.utils import timezone
from django.utils.formats import date_format
from drf_haystack.serializers import HaystackSerializer
from .search_indexes import PosteoIndex

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nombre', 'apellido', 'piso', 'numero']


class TipoPosteoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPosteo
        fields = ['id', 'tipo']
        
class RespuestaSerializer(serializers.ModelSerializer):
    usuario = UserDetailSerializer(read_only=True)
    fecha_creacion_legible = serializers.SerializerMethodField()

    class Meta:
        model = Respuesta
        fields = ['id', 'usuario', 'contenido', 'fecha_creacion_legible']
        read_only_fields = ['usuario', 'fecha_creacion_legible']

    def get_fecha_creacion_legible(self, obj):
        return date_format(timezone.localtime(obj.fecha_creacion), format="DATETIME_FORMAT")


class PosteoSerializer(serializers.ModelSerializer):
    tipo_posteo = TipoPosteoSerializer(read_only=True)
    tipo_posteo_id = serializers.PrimaryKeyRelatedField(queryset=TipoPosteo.objects.all(), source='tipo_posteo', write_only=True)
    usuario = UserDetailSerializer(read_only=True)
    fecha_creacion_legible = serializers.SerializerMethodField()
    respuestas = RespuestaSerializer(many=True, read_only=True)

    class Meta:
        model = Posteo
        fields = ['id', 'titulo', 'descripcion', 'usuario', 'tipo_posteo', 'tipo_posteo_id', 'imagen', 'fecha_creacion_legible', 'respuestas']
        read_only_fields = ['usuario', 'fecha_creacion_legible', 'respuestas']

    def get_fecha_creacion_legible(self, obj):
        return date_format(timezone.localtime(obj.fecha_creacion), format="DATETIME_FORMAT")

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)
    
class PosteoSearchSerializer(HaystackSerializer):
    object = PosteoSerializer(read_only=True)

    class Meta:
        index_classes = [PosteoIndex]
        fields = ['text', 'titulo', 'descripcion', 'edificio', 'object']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.object:
            rep['object'] = PosteoSerializer(instance.object).data
        return rep


class TipoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEvento
        fields = ['id', 'tipo']
        
class EventoSerializer(serializers.ModelSerializer):
    fecha_inicio = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    fecha_fin = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    tipo_evento = TipoEventoSerializer(read_only=True)
    tipo_evento_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoEvento.objects.all(),
        source='tipo_evento',
        write_only=True
    )
    
    class Meta:
        model = Evento
        fields = ['id', 'titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'usuario', 'tipo_evento', 'tipo_evento_id']
        read_only_fields = ['usuario']
    
    def validate(self, data):
        # Obtengo los valores actuales del evento si es una actualizacion
        instance = getattr(self, 'instance', None)
        fecha_inicio = data.get('fecha_inicio', instance.fecha_inicio if instance else None)
        fecha_fin = data.get('fecha_fin', instance.fecha_fin if instance else None)
        
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise serializers.ValidationError('La fecha y hora de fin debe ser igual o posterior a la fecha y hora de inicio.')
        return data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['fecha_inicio'] = timezone.localtime(instance.fecha_inicio).strftime("%Y-%m-%d %H:%M:%S")
        representation['fecha_fin'] = timezone.localtime(instance.fecha_fin).strftime("%Y-%m-%d %H:%M:%S")
        return representation
    
class EventoCalendarioSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(source='fecha_inicio')
    end = serializers.DateTimeField(source='fecha_fin')
    
    class Meta:
        model = Evento
        fields = ['id', 'titulo', 'start', 'end', 'descripcion']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['titulo'] = instance.titulo
        return data


