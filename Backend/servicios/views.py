from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import TipoServicio, Servicio
from .serializers import TipoServicioSerializer, ServicioSerializer, ServicioListSerializer
from rest_framework.permissions import IsAuthenticated
from .permisos import IsColaboradorEdificio, CanViewServicios


class TipoServicioViewSet(viewsets.ModelViewSet):
    queryset = TipoServicio.objects.all()
    serializer_class = TipoServicioSerializer
    permission_classes = [IsAuthenticated]

class ServicioViewSet(viewsets.ModelViewSet):
    serializer_class = ServicioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo']

    def get_permissions(self):
        """
        CRUD completo para Colaboradores en su edificio
        Solo lectura para Inquilinos y Dueños de su edificio
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsColaboradorEdificio]
        else:
            permission_classes = [IsAuthenticated, CanViewServicios]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # Filtra los servicios según el edificio del usuario.
        user = self.request.user
        if user.edificio:
            return Servicio.objects.filter(edificio=user.edificio)
        return Servicio.objects.none()

    def get_serializer_class(self):
        # Uso un serializer diferente para listar servicios
        if self.action == 'list':
            return ServicioListSerializer
        return ServicioSerializer

    def perform_create(self, serializer):
        # Asigna automáticamente el edificio del colaborador al servicio
        serializer.save(edificio=self.request.user.edificio)

    @action(detail=False, methods=['GET'])
    def por_tipo(self, request):
        # Endpoint para filtrar servicios por tipo en el edificio del usuario
        tipo_id = request.query_params.get('tipo_id')
        if not tipo_id:
            return Response(
                {"error": "Se requiere el parámetro tipo_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        servicios = self.get_queryset().filter(tipo_id=tipo_id)
        serializer = ServicioListSerializer(servicios, many=True)
        return Response(serializer.data)