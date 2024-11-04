from rest_framework import permissions

class IsColaboradorEdificio(permissions.BasePermission):
    # Permite acceso solo a usuarios con rol 'Colaborador' del mismo edificio.
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.rol.rol == 'Colaborador'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        # Verifica que el servicio pertenezca al edificio del colaborador
        return obj.edificio == request.user.edificio

class CanViewServicios(permissions.BasePermission):
    # Permite ver servicios a usuarios con rol 'Inquilino' o 'Duenio' del mismo edificio.
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.rol.rol in ['Inquilino', 'Duenio', 'Colaborador']

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        # Verifica que el usuario pertenezca al mismo edificio que el servicio
        return obj.edificio == request.user.edificio

