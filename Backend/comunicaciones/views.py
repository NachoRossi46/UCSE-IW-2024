from rest_framework import viewsets, permissions, generics, status, parsers
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters import rest_framework as filters
# from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import OrderingFilter
from .models import Posteo, TipoPosteo
from .serializers import PosteoSerializer, TipoPosteoSerializer
import boto3
from botocore.exceptions import ClientError

class IsAuthenticatedWithCustomMessage(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return True

    def message(self, request):
        return "ERROR, no estas autenticado."
    
class PosteoFilter(filters.FilterSet):
    tipo_posteo = filters.CharFilter(field_name='tipo_posteo__tipo')
    usuario = filters.CharFilter(field_name='usuario__email')

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
        return Posteo.objects.filter(usuario__edificio=user.edificio)

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


