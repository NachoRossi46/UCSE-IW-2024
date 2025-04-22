import datetime
import logging
import time
from time import timezone
from rest_framework import viewsets, permissions, generics, status, parsers
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters import rest_framework as filters
# from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from .models import Posteo, TipoPosteo, Respuesta, Evento
from .serializers import PosteoSerializer, TipoPosteoSerializer, RespuestaSerializer, EventoSerializer, EventoCalendarioSerializer, PosteoSearchSerializer
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from usuarios.models import User
from django.core.mail import send_mass_mail
from rest_framework.decorators import api_view
from django.core.management import call_command
from django.http import HttpResponse
from drf_haystack.viewsets import HaystackViewSet
from haystack.query import SearchQuerySet

logger = logging.getLogger(__name__)

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
        
class TimingMixin:
    """Mixin para añadir logging de tiempos a los métodos de las vistas"""
    
    def dispatch(self, request, *args, **kwargs):
        # Medir el tiempo total de la vista
        start_time = time.time()
        response = super().dispatch(request, *args, **kwargs)
        total_time = time.time() - start_time
        
        # Loggear el tiempo total
        logger.info(f"{self.__class__.__name__} {request.method} {request.path}: {total_time:.4f}s")
        
        # Agregar tiempo a la respuesta para debugging (opcional)
        if isinstance(response, Response) and settings.DEBUG:
            if not response.data:
                response.data = {}
            if isinstance(response.data, dict):
                response.data['processing_time'] = f"{total_time:.4f}s"
                
        return response

class PosteoViewSet(viewsets.ModelViewSet):
    serializer_class = PosteoSerializer
    permission_classes = [IsAuthenticatedWithCustomMessage]
    filterset_class = PosteoFilter
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['fecha_creacion']
    ordering = ['-fecha_creacion']
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)

    def get_queryset(self):
        # Medir el tiempo de ejecución de la consulta
        start_time = time.time()
        user = self.request.user
        queryset = Posteo.objects.filter(usuario__edificio=user.edificio)
        
        usuario_id = self.request.query_params.get('usuario')
        if usuario_id:
            queryset = queryset.filter(usuario__id=usuario_id)
        
        tipo_posteo = self.request.query_params.get('tipo_posteo')
        if tipo_posteo:
            queryset = queryset.filter(tipo_posteo__tipo=tipo_posteo)
            
        # tiempos de consulta
        query_time = time.time() - start_time
        logger.info(f"PosteoViewSet.get_queryset tiempo: {query_time:.4f}s | Params: {self.request.query_params}")
        
        return queryset

    def perform_create(self, serializer):
        start_time = time.time()
        instance = serializer.save(usuario=self.request.user)
        create_time = time.time() - start_time
        logger.info(f"PosteoViewSet.perform_create tiempo: {create_time:.4f}s | Posteo ID: {instance.id}")

    def perform_update(self, serializer):
        start_time = time.time()
        if serializer.instance.usuario == self.request.user:
            instance = serializer.save()
            update_time = time.time() - start_time
            logger.info(f"PosteoViewSet.perform_update tiempo: {update_time:.4f}s | Posteo ID: {instance.id}")
        else:
            raise PermissionDenied("No tienes permiso para editar este posteo.")

    def perform_destroy(self, instance):
        start_time = time.time()
        if instance.usuario == self.request.user:
            try:
                # Si tienes una imagen asociada, elimínala de S3
                if instance.imagen:
                    s3_delete_start = time.time()
                    instance.imagen.delete(save=False)
                    s3_delete_time = time.time() - s3_delete_start
                    logger.info(f"S3 delete tiempo: {s3_delete_time:.4f}s | Posteo ID: {instance.id}")
                
                instance.delete()
                total_delete_time = time.time() - start_time
                logger.info(f"PosteoViewSet.perform_destroy tiempo total: {total_delete_time:.4f}s | Posteo ID: {instance.id}")
            except ClientError as e:
                error_time = time.time() - start_time
                logger.error(f"S3 ClientError: {str(e)} | Tiempo: {error_time:.4f}s")
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

class PosteoSearchViewSet(HaystackViewSet):
    index_models = [Posteo]
    serializer_class = PosteoSearchSerializer

    def get_queryset(self, *args, **kwargs):
        start_time = time.time()
        queryset = SearchQuerySet().models(Posteo)
        user = self.request.user
        
        # Filtro por edificio si el usuario está autenticado
        if user.is_authenticated:
            queryset = queryset.filter(edificio=user.edificio.id)

        # Aplico el termino de busqueda
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.auto_query(query)

        query_time = time.time() - start_time
        logger.info(f"PosteoSearchViewSet.get_queryset tiempo: {query_time:.4f}s | Query: {query}")
        
        return queryset.load_all()

@api_view(['GET'])
def rebuild_index(request):
    try:
        call_command("rebuild_index", interactive=False)
        result = "Index rebuilt"
    except Exception as err:
        result = f"Error: {err}"
    return Response({"result": result})

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")



class RespuestaViewSet(viewsets.ModelViewSet):
    serializer_class = RespuestaSerializer
    permission_classes = [IsAuthenticatedWithCustomMessage]

    def get_queryset(self):
        start_time = time.time()
        queryset = Respuesta.objects.filter(posteo__usuario__edificio=self.request.user.edificio)
        query_time = time.time() - start_time
        logger.info(f"RespuestaViewSet.get_queryset tiempo: {query_time:.4f}s")
        return queryset

    def perform_create(self, serializer):
        start_time = time.time()
        posteo_id = self.kwargs.get('posteo_pk')
        posteo = Posteo.objects.get(pk=posteo_id)
        instance = serializer.save(usuario=self.request.user, posteo=posteo)
        create_time = time.time() - start_time
        logger.info(f"RespuestaViewSet.perform_create tiempo: {create_time:.4f}s | Respuesta ID: {instance.id} | Posteo ID: {posteo_id}")

    def perform_update(self, serializer):
        start_time = time.time()
        if serializer.instance.usuario == self.request.user:
            instance = serializer.save()
            update_time = time.time() - start_time
            logger.info(f"RespuestaViewSet.perform_update tiempo: {update_time:.4f}s | Respuesta ID: {instance.id}")
        else:
            raise PermissionDenied("No tienes permiso para editar esta respuesta.")

    def perform_destroy(self, instance):
        start_time = time.time()
        if instance.usuario == self.request.user:
            instance.delete()
            delete_time = time.time() - start_time
            logger.info(f"RespuestaViewSet.perform_destroy tiempo: {delete_time:.4f}s | Respuesta ID: {instance.id}")
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
    start_time = time.time()
    
    usuarios = User.objects.filter(edificio=evento.usuario.edificio).exclude(id=evento.usuario.id)
    
    query_time = time.time() - start_time
    logger.info(f"enviar_notificaciones_evento query usuarios tiempo: {query_time:.4f}s | Cantidad usuarios: {usuarios.count()}")
    email_start_time = time.time()
    
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
    
    try:
        send_mass_mail(messages, fail_silently=False)
        email_time = time.time() - email_start_time
        logger.info(f"enviar_notificaciones_evento envío emails tiempo: {email_time:.4f}s | Emails enviados: {len(messages)}")
    except Exception as e:
        email_time = time.time() - email_start_time
        logger.error(f"Error al enviar emails: {str(e)} | Tiempo: {email_time:.4f}s")
    
    total_time = time.time() - start_time
    logger.info(f"enviar_notificaciones_evento tiempo total: {total_time:.4f}s | Evento ID: {evento.id}")


class EventoViewSet(viewsets.ModelViewSet):
    serializer_class = EventoSerializer
    
    def get_queryset(self):
        start_time = time.time()
        queryset = Evento.objects.filter(usuario__edificio=self.request.user.edificio)
        query_time = time.time() - start_time
        logger.info(f"EventoViewSet.get_queryset tiempo: {query_time:.4f}s")
        return queryset

    def perform_create(self, serializer):
        start_time = time.time()
        evento = serializer.save(usuario=self.request.user)
        save_time = time.time() - start_time
        logger.info(f"EventoViewSet.perform_create save tiempo: {save_time:.4f}s | Evento ID: {evento.id}")
        
        notification_start = time.time()
        enviar_notificaciones_evento(evento)
        notification_time = time.time() - notification_start
        logger.info(f"EventoViewSet.perform_create notificaciones tiempo: {notification_time:.4f}s | Evento ID: {evento.id}")
        
        total_time = time.time() - start_time
        logger.info(f"EventoViewSet.perform_create tiempo total: {total_time:.4f}s | Evento ID: {evento.id}")
    
    def create(self, request, *args, **kwargs):
        start_time = time.time()
        serializer = self.get_serializer(data=request.data)
        validation_time = time.time()
        serializer.is_valid(raise_exception=True)
        validation_time = time.time() - validation_time
        logger.info(f"EventoViewSet.create validación tiempo: {validation_time:.4f}s")
        
        perform_time = time.time()
        self.perform_create(serializer)
        perform_time = time.time() - perform_time
        logger.info(f"EventoViewSet.create perform_create tiempo: {perform_time:.4f}s")
        
        headers = self.get_success_headers(serializer.data)
        total_time = time.time() - start_time
        logger.info(f"EventoViewSet.create tiempo total: {total_time:.4f}s")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def perform_update(self, serializer):
        start_time = time.time()
        if serializer.instance.usuario == self.request.user:
            instance = serializer.save()
            update_time = time.time() - start_time
            logger.info(f"EventoViewSet.perform_update tiempo: {update_time:.4f}s | Evento ID: {instance.id}")
        else:
            raise PermissionDenied("No tienes permiso para editar este evento.")
        
    def perform_destroy(self, instance):
        start_time = time.time()
        if instance.usuario == self.request.user:
            instance.delete()
            delete_time = time.time() - start_time
            logger.info(f"EventoViewSet.perform_destroy tiempo: {delete_time:.4f}s | Evento ID: {instance.id}")
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
