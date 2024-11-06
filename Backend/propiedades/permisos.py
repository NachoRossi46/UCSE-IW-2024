from rest_framework import permissions

class EdificioPermission(permissions.BasePermission):
    """
    Permisos personalizados para Edificio:
    - GET: público, no requiere autenticación
    - POST: solo administradores desde el admin de Django
    - PUT/PATCH/DELETE: solo administradores
    """
    def has_permission(self, request, view):
        # GET permitido sin autenticación
        if request.method == 'GET':
            return True
            
        # Para otros métodos, verificar autenticación
        if not request.user.is_authenticated:
            return False
            
        # Solo administradores pueden hacer modificaciones
        if request.user.is_superuser or request.user.rol.rol == 'Administrador':
            return True
            
        return False

    def has_object_permission(self, request, view, obj):
        # GET permitido sin autenticación
        if request.method == 'GET':
            return True
            
        # Solo administradores pueden modificar objetos
        if request.user.is_authenticated and (request.user.is_superuser or request.user.rol.rol == 'Administrador'):
            return True
            
        return False