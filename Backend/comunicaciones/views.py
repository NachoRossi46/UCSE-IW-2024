import datetime
from time import timezone
from rest_framework import viewsets, permissions, generics, status, parsers
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters import rest_framework as filters
# from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from .models import Posteo, TipoPosteo, Respuesta, Evento
from .serializers import PosteoSerializer, TipoPosteoSerializer, RespuestaSerializer, EventoSerializer, EventoCalendarioSerializer
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from usuarios.models import User
from django.core.mail import send_mass_mail

class IsAuthenticatedWithCustomMessage(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return True

    def message(self, request):
        return "ERROR, no estas autenticado."
    
class PosteoFilter(filters.FilterSet):
    tipo_posteo = filters.CharFilter(field_name='tipo_posteo__tipo')
    usuario = filters.NumberFilter(field_name='usuario__id')

    class Meta:
        model = Posteo
        fields = ['tipo_posteo', 'usuario']

class PosteoViewSet(viewsets.ModelViewSet):
    serializer_class = PosteoSerializer
    permission_classes = [IsAuthenticatedWithCustomMessage]
    filterset_class = PosteoFilter
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['fecha_creacion']
    ordering = ['-fecha_creacion']
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)

    def get_queryset(self):
        user = self.request.user
        queryset = Posteo.objects.filter(usuario__edificio=user.edificio)
        
        usuario_id = self.request.query_params.get('usuario')
        if usuario_id:
            queryset = queryset.filter(usuario__id=usuario_id)
        
        tipo_posteo = self.request.query_params.get('tipo_posteo')
        if tipo_posteo:
            queryset = queryset.filter(tipo_posteo__tipo=tipo_posteo)
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.usuario == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para editar este posteo.")

    def perform_destroy(self, instance):
        if instance.usuario == self.request.user:
            try:
                # Si tienes una imagen asociada, elimínala de S3
                if instance.imagen:
                    instance.imagen.delete(save=False)
                instance.delete()
            except ClientError as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            raise PermissionDenied("No tienes permiso para eliminar este posteo.")
    
    def handle_exception(self, exc):
        if isinstance(exc, permissions.PermissionDenied):
            return Response(
                {"detail": self.permission_classes[0]().message(self.request)},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)


class RespuestaViewSet(viewsets.ModelViewSet):
    serializer_class = RespuestaSerializer
    permission_classes = [IsAuthenticatedWithCustomMessage]

    def get_queryset(self):
        return Respuesta.objects.filter(posteo__usuario__edificio=self.request.user.edificio)

    def perform_create(self, serializer):
        posteo_id = self.kwargs.get('posteo_pk')
        posteo = Posteo.objects.get(pk=posteo_id)
        serializer.save(usuario=self.request.user, posteo=posteo)

    def perform_update(self, serializer):
        if serializer.instance.usuario == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para editar esta respuesta.")

    def perform_destroy(self, instance):
        if instance.usuario == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("No tienes permiso para eliminar esta respuesta.")

class TipoPosteoListView(generics.ListAPIView):
    queryset = TipoPosteo.objects.all()
    serializer_class = TipoPosteoSerializer
    permission_classes = [IsAuthenticatedWithCustomMessage]

    def handle_exception(self, exc):
        if isinstance(exc, permissions.PermissionDenied):
            return Response(
                {"detail": self.permission_classes[0]().message(self.request)},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)

def enviar_notificaciones_evento(evento):
    usuarios = User.objects.filter(edificio=evento.usuario.edificio).exclude(id=evento.usuario.id)
    subject = f"Nuevo evento: {evento.titulo}"
    message = f"""
    Se ha creado un nuevo evento en tu edificio:
    
    Título: {evento.titulo}
    Descripción: {evento.descripcion}
    Fecha de inicio: {evento.fecha_inicio}
    Fecha de fin: {evento.fecha_fin}
    Creado por: {evento.usuario.nombre} {evento.usuario.apellido}
    
    Para más detalles, ingresa a la aplicación.
    """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [usuario.email for usuario in usuarios]
    
    # Creo una tupla para cada email
    messages = [(subject, message, from_email, [email]) for email in recipient_list]
    
    send_mass_mail(messages, fail_silently=False)

class EventoViewSet(viewsets.ModelViewSet):
    serializer_class = EventoSerializer
    
    def get_queryset(self):
        return Evento.objects.filter(usuario__edificio=self.request.user.edificio)

    def perform_create(self, serializer):
        evento = serializer.save(usuario=self.request.user)
        enviar_notificaciones_evento(evento)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def perform_update(self, serializer):
        if serializer.instance.usuario == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para editar este evento.")
        
    def perform_destroy(self, instance):
        if instance.usuario == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("No tienes permiso para eliminar esta evento.")
        
    @action(detail=False, methods=['get'])
    def calendario(self, request):
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        
        if start and end:
            start_date = timezone.make_aware(datetime.fromisoformat(start))
            end_date = timezone.make_aware(datetime.fromisoformat(end))
            queryset = self.get_queryset().filter(
                fecha_inicio__lt=end_date,
                fecha_fin__gt=start_date
            )
        else:
            queryset = self.get_queryset()

        serializer = EventoCalendarioSerializer(queryset, many=True)
        return Response(serializer.data)
