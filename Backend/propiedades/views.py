from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Edificio
from .serializers import EdificioSerializer, EdificioDetailSerializer
from .permisos import EdificioPermission

class EdificioViewSet(viewsets.ModelViewSet):
    queryset = Edificio.objects.all()
    permission_classes = [EdificioPermission]
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'servicios']:
            return EdificioDetailSerializer
        return EdificioSerializer
    
    def get_queryset(self):
        queryset = Edificio.objects.all()
        if self.action in ['retrieve', 'servicios']:
            queryset = queryset.prefetch_related('usuarios', 'servicios')
        return queryset

    # Deshabilitar la creación vía API
    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "La creación de edificios solo está permitida desde el panel de administración."},
            status=405
        )
    
    @action(detail=True, methods=['GET'])
    def servicios(self, request, pk=None):
        edificio = self.get_object()
        serializer = EdificioDetailSerializer(
            edificio, 
            context={'include_services': True}
        )
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def usuarios(self, request, pk=None):
        edificio = self.get_object()
        from usuarios.serializers import UserSerializer
        usuarios = edificio.usuarios.all()
        serializer = UserSerializer(usuarios, many=True)
        return Response(serializer.data)