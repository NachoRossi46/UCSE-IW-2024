from rest_framework import permissions

class EdificioPermission(permissions.BasePermission):
    """
    Permisos personalizados para Edificio.
    - Administradores pueden hacer todo
    - Colaboradores pueden ver detalles de su edificio
    - Inquilinos y Dueños pueden ver detalles de su edificio
    """
    def has_permission(self, request, view):
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            return False

        # Administradores pueden hacer todo
        if request.user.is_superuser or request.user.rol.rol == 'Administrador':
            return True

        # Para otros roles, solo permitir GET
        if request.method in permissions.SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Administradores pueden hacer todo
        if request.user.is_superuser or request.user.rol.rol == 'Administrador':
            return True

        # Usuarios solo pueden ver su propio edificio
        if request.method in permissions.SAFE_METHODS:
            return request.user.edificio == obj

        return False
