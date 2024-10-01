from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import TipoServicio, Servicio
from .serializers import TipoServicioSerializer, ServicioSerializer, ServicioEdificioSerializer
from propiedades.models import Edificio


class TipoServicioViewSet(viewsets.ModelViewSet):
    queryset = TipoServicio.objects.all()
    serializer_class = TipoServicioSerializer

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo']

    @action(detail=False, methods=['GET'])
    def por_edificio(self, request):
        edificio_id = request.query_params.get('edificio_id')
        tipo_id = request.query_params.get('tipo_id')
        
        if not edificio_id:
            return Response({"error": "Se requiere el parámetro edificio_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            edificio = Edificio.objects.get(id=edificio_id)
        except Edificio.DoesNotExist:
            return Response({"error": "Edificio no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        servicios = edificio.servicios.all()
        if tipo_id:
            servicios = servicios.filter(tipo_id=tipo_id)
            
        serializer = ServicioEdificioSerializer(servicios, many=True)
        return Response(serializer.data)