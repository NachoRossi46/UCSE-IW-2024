from rest_framework import serializers
from .models import Conversacion, Mensaje
from usuarios.serializers import UserSerializer
from usuarios.models import User
from django.utils.formats import date_format
from django.utils import timezone

class MensajeSerializer(serializers.ModelSerializer):
    remitente = UserSerializer(read_only=True)
    fecha_envio_legible = serializers.SerializerMethodField()

    class Meta:
        model = Mensaje
        fields = ['id', 'remitente', 'contenido', 'fecha_envio_legible', 'leido']
        read_only_fields = ['remitente', 'fecha_envio_legible', 'leido']
    
    def get_fecha_envio_legible(self, obj):
        return date_format(timezone.localtime(obj.fecha_envio), format="DATETIME_FORMAT")

class ConversacionSerializer(serializers.ModelSerializer):
    participantes = UserSerializer(many=True, read_only=True)
    ultimo_mensaje = serializers.SerializerMethodField()
    fecha_creacion_legible = serializers.SerializerMethodField()
    fecha_utlima_actualizacion_legible = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversacion
        fields = ['id', 'participantes', 'fecha_creacion_legible', 'fecha_utlima_actualizacion_legible', 'ultimo_mensaje']
        read_only_fields = ['fecha_creacion_legible', 'fecha_utlima_actualizacion_legible']

    def get_ultimo_mensaje(self, obj):
        ultimo_mensaje = obj.mensajes.last()
        if ultimo_mensaje:
            return MensajeSerializer(ultimo_mensaje).data
        return None
    
    def get_fecha_creacion_legible(self, obj):
        return date_format(timezone.localtime(obj.fecha_creacion), format="DATETIME_FORMAT")
    
    def get_fecha_utlima_actualizacion_legible(self, obj):
        return date_format(timezone.localtime(obj.ultima_actualizacion), format="DATETIME_FORMAT")

class ConversacionCreateSerializer(serializers.ModelSerializer):
    participante_id = serializers.IntegerField(write_only=True)
    mensaje_inicial = serializers.CharField(write_only=True)

    class Meta:
        model = Conversacion
        fields = ['participante_id', 'mensaje_inicial']

    def validate_participante_id(self, value):
        try:
            participante = User.objects.get(id=value)
            # Verificar que el participante sea del mismo edificio
            if participante.edificio != self.context['request'].user.edificio:
                raise serializers.ValidationError("Solo puedes iniciar conversaciones con usuarios de tu mismo edificio.")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuario no encontrado.")
