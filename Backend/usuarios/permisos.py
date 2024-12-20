from rest_framework import permissions

class IsOwnerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Permitir listar a todos
        if view.action == 'list':
            return True
        # Para otras acciones, requerir autenticación
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Verificar que el usuario autenticado sea el dueño del objeto
        return obj.id == request.user.id