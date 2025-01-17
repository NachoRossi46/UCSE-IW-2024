from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Conversacion, Mensaje
from usuarios.models import User
from .serializers import ConversacionSerializer, MensajeSerializer, ConversacionCreateSerializer, UserSerializer
from .permisos import EsParticipante

class ConversacionViewSet(viewsets.ModelViewSet):
    serializer_class = ConversacionSerializer
    permission_classes = [IsAuthenticated, EsParticipante]

    @action(detail=False, methods=['GET'])
    def usuarios_disponibles(self, request):
        """Lista los usuarios del mismo edificio disponibles para chatear."""
        usuarios = User.objects.filter(
            edificio=request.user.edificio
        ).exclude(
            id=request.user.id  # Excluir al usuario actual
        )
        return Response(
            UserSerializer(usuarios, many=True).data
        )

    def get_queryset(self):
        return Conversacion.objects.filter(participantes=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversacionCreateSerializer
        return ConversacionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Crear conversación
        conversacion = Conversacion.objects.create()
        conversacion.participantes.add(request.user)
        conversacion.participantes.add(serializer.validated_data['participante_id'])
        
        # Crear mensaje inicial
        Mensaje.objects.create(
            conversacion=conversacion,
            remitente=request.user,
            contenido=serializer.validated_data['mensaje_inicial']
        )
        
        return Response(
            ConversacionSerializer(conversacion).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['POST'])
    def enviar_mensaje(self, request, pk=None):
        conversacion = self.get_object()
        contenido = request.data.get('contenido')
        
        if not contenido:
            return Response(
                {'error': 'El contenido del mensaje es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        mensaje = Mensaje.objects.create(
            conversacion=conversacion,
            remitente=request.user,
            contenido=contenido
        )
        
        conversacion.ultima_actualizacion = mensaje.fecha_envio
        conversacion.save()
        
        return Response(
            MensajeSerializer(mensaje).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['GET'])
    def mensajes(self, request, pk=None):
        conversacion = self.get_object()
        mensajes = conversacion.mensajes.all()
        
        # Marcar como leídos los mensajes no leídos
        mensajes.filter(
            ~Q(remitente=request.user),
            leido=False
        ).update(leido=True)
        
        return Response(
            MensajeSerializer(mensajes, many=True).data
        )
