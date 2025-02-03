from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from .models import Denuncia
from .serializers import DenunciaSerializer, CrearDenunciaSerializer
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

class EsColaborador(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.rol.rol == 'Colaborador'

class DenunciaFilter(django_filters.FilterSet):
    estado = django_filters.ChoiceFilter(choices=Denuncia.ESTADO_CHOICES)
    tipo = django_filters.ChoiceFilter(choices=Denuncia.TIPO_CHOICES)
    fecha_creacion = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Denuncia
        fields = ['estado', 'tipo', 'fecha_creacion']
        
def validate_state_transition(current_state, new_state):
    valid_transitions = {
        'pendiente': ['en_revision'],
        'en_revision': ['resuelta', 'desestimada'],
        'resuelta': [],
        'desestimada': []
    }
    
    if new_state not in valid_transitions[current_state]:
        raise ValidationError(
            f"No se puede cambiar el estado de '{current_state}' a '{new_state}'"
        )

class DenunciaViewSet(viewsets.ModelViewSet):
    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = DenunciaFilter
    ordering_fields = ['fecha_creacion', 'estado']
    ordering = ['-fecha_creacion']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [EsColaborador]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Denuncia.objects.filter(
            denunciante__edificio=self.request.user.edificio
        ).select_related(
            'denunciante',
            'usuario_denunciado',
            'posteo_denunciado',
            'evento_denunciado'
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return CrearDenunciaSerializer
        return DenunciaSerializer

    def perform_create(self, serializer):
        serializer.save(denunciante=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
                return Response(
                    {
                        'message': 'Denuncia creada exitosamente',
                        'denuncia': serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, *args, **kwargs):
        return Response(
            {'error': 'No se permite modificar denuncias'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {'error': 'No se permite modificar denuncias'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {'error': 'No se permite eliminar denuncias'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    @action(detail=True, methods=['PATCH'])
    def cambiar_estado(self, request, pk=None):
        denuncia = self.get_object()
        nuevo_estado = request.data.get('estado')

        if not nuevo_estado:
            return Response(
                {'error': 'Debe especificar el nuevo estado'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_state_transition(denuncia.estado, nuevo_estado)
            denuncia.estado = nuevo_estado
            denuncia.save()
            
            return Response({
                'message': 'Estado actualizado correctamente',
                'denuncia': DenunciaSerializer(denuncia).data
            })
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

