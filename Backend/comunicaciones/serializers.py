from rest_framework import serializers
from .models import Posteo, TipoPosteo, Respuesta, TipoEvento, Evento
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
        # Obtener los valores actuales del evento si estamos en una actualización
        instance = getattr(self, 'instance', None)
        fecha_inicio = data.get('fecha_inicio', instance.fecha_inicio if instance else None)
        fecha_fin = data.get('fecha_fin', instance.fecha_fin if instance else None)
        
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise serializers.ValidationError('La fecha y hora de fin debe ser igual o posterior a la fecha y hora de inicio.')
        return data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['fecha_inicio'] = date_format(timezone.localtime(instance.fecha_inicio), format="DATETIME_FORMAT")
        representation['fecha_fin'] = date_format(timezone.localtime(instance.fecha_fin), format="DATETIME_FORMAT")
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


