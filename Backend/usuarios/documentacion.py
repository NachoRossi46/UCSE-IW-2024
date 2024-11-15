from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .serializers import UserSerializer, UserRegistrationSerializer

# Schemas para AuthViewSet
auth_schema = extend_schema_view(
    registro=extend_schema(
        summary="Registro de nuevo usuario",
        description="Crea un nuevo usuario en el sistema. El usuario quedará inactivo hasta que sea activado por un administrador.",
        request=UserRegistrationSerializer,
        responses={
            201: OpenApiResponse(
                description="Usuario creado exitosamente",
                examples=[
                    OpenApiExample(
                        "Éxito",
                        value={
                            "user": {
                                "email": "usuario@ejemplo.com",
                                "nombre": "Juan",
                                "apellido": "Pérez",
                                "rol": 1,
                                "edificio": 1,
                                "piso": 2,
                                "numero": "A"
                            },
                            "message": "Usuario creado exitosamente. Por favor, espere la activación de su cuenta."
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Error en la validación de datos",
                examples=[
                    OpenApiExample(
                        "Error",
                        value={
                            "email": ["Este campo es requerido."],
                            "password": ["La contraseña es demasiado corta."]
                        }
                    )
                ]
            )
        }
    ),
    login=extend_schema(
        summary="Iniciar sesión",
        description="Autenticación de usuario y generación de token",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'format': 'email'},
                    'password': {'type': 'string', 'format': 'password'}
                },
                'required': ['email', 'password']
            }
        },
        responses={
            200: OpenApiResponse(
                description="Login exitoso",
                examples=[
                    OpenApiExample(
                        "Éxito",
                        value={
                            "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
                            "user_id": 1,
                            "email": "usuario@ejemplo.com"
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Credenciales inválidas"),
            403: OpenApiResponse(description="Cuenta inactiva")
        }
    ),
    logout=extend_schema(
        summary="Cerrar sesión",
        description="Invalida el token de autenticación actual",
        responses={
            200: OpenApiResponse(
                description="Logout exitoso",
                examples=[
                    OpenApiExample(
                        "Éxito",
                        value={"message": "Logout exitoso."}
                    )
                ]
            ),
            400: OpenApiResponse(description="Error al cerrar sesión")
        }
    )
)

# Schemas para UserViewSet
user_schema = extend_schema_view(
    list=extend_schema(
        summary="Listar usuarios",
        description="Obtiene la lista de todos los usuarios registrados en el sistema",
        parameters=[
            OpenApiParameter(
                name='rol',
                description='Filtrar por rol de usuario',
                required=False,
                type=str,
                examples=[
                    OpenApiExample('Inquilino', value='Inquilino'),
                    OpenApiExample('Duenio', value='Duenio')
                ]
            ),
            OpenApiParameter(
                name='edificio',
                description='Filtrar por ID de edificio',
                required=False,
                type=int
            )
        ]
    ),
    create=extend_schema(
        summary="Crear usuario",
        description="Crea un nuevo usuario en el sistema (solo administradores)",
        request=UserSerializer,
        responses={
            201: UserSerializer,
            400: OpenApiResponse(description="Error en los datos proporcionados")
        }
    ),
    retrieve=extend_schema(
        summary="Obtener usuario",
        description="Obtiene los detalles de un usuario específico",
        responses={
            200: UserSerializer,
            404: OpenApiResponse(description="Usuario no encontrado")
        }
    ),
    update=extend_schema(
        summary="Actualizar usuario",
        description="Actualiza todos los campos de un usuario existente",
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Error en los datos proporcionados"),
            404: OpenApiResponse(description="Usuario no encontrado")
        }
    ),
    partial_update=extend_schema(
        summary="Actualizar usuario parcialmente",
        description="Actualiza uno o más campos de un usuario existente",
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Error en los datos proporcionados"),
            404: OpenApiResponse(description="Usuario no encontrado")
        }
    ),
    destroy=extend_schema(
        summary="Eliminar usuario",
        description="Elimina un usuario del sistema",
        responses={
            204: OpenApiResponse(description="Usuario eliminado exitosamente"),
            404: OpenApiResponse(description="Usuario no encontrado")
        }
    )
)
