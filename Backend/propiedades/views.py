from rest_framework import viewsets
from .models import Edificio
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import EdificioSerializer, EdificioDetailSerializer
from .models import Edificio

class EdificioViewSet(viewsets.ModelViewSet):
    queryset = Edificio.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'servicios']:
            return EdificioDetailSerializer
        return EdificioSerializer

    def get_queryset(self):
        queryset = Edificio.objects.all()
        if self.action in ['retrieve', 'servicios']:
            queryset = queryset.prefetch_related('usuarios', 'servicios')
        return queryset

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



