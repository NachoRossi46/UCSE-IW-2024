from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Posteo, TipoPosteo
from .serializers import PosteoSerializer, TipoPosteoSerializer

class IsAuthenticatedWithCustomMessage(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return True

    def message(self, request):
        return "ERROR, no estas autenticado."


class PosteoViewSet(viewsets.ModelViewSet):
    serializer_class = PosteoSerializer
    permission_classes = [IsAuthenticatedWithCustomMessage]

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
        instance.delete()
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


