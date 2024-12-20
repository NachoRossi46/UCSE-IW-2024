from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail import send_mail
from .models import User, PasswordResetToken
from .permisos import IsOwnerUser  
from .serializers import UserSerializer, UserRegistrationSerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer, UserUpdateProfileSerializer
from drf_spectacular.utils import extend_schema
from .documentacion import auth_schema, user_schema

@auth_schema
@extend_schema(tags=['autenticación'])
class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['POST'])
    def registro(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                validate_password(request.data.get('password'))
            except ValidationError as e:
                return Response({"password": e.messages}, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.save()
            return Response({
                "user": UserRegistrationSerializer(user).data,
                "message": "Usuario creado exitosamente. Por favor, espere la activación de su cuenta."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "La cuenta no está activa."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Credenciales inválidas."}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "Logout exitoso."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['POST'])
    def request_password_reset(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = PasswordResetToken.objects.create(user=user)
                
                # Contenido del email
                subject = 'Recuperación de Contraseña'
                message = f'''
                Hola {user.nombre},

                Has solicitado restablecer tu contraseña. Por favor, utiliza el siguiente código para completar el proceso:

                {token.token}

                Este código expirará en 1 hora.

                Si no solicitaste este cambio, puedes ignorar este correo.
                '''

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                return Response({
                    "message": "Se ha enviado un correo con las instrucciones para restablecer tu contraseña."
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                # Por seguridad, no revelamos si el email existe o no
                return Response({
                    "message": "Si el correo existe en nuestro sistema, recibirás las instrucciones para restablecer tu contraseña."
                }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def reset_password(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token_obj = PasswordResetToken.objects.get(
                    token=serializer.validated_data['token'],
                    user__email=serializer.validated_data['email'],
                    is_used=False
                )
                
                if not token_obj.is_valid():
                    return Response({
                        "error": "El token ha expirado."
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Cambiar la contraseña
                user = token_obj.user
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                
                # Marcar el token como usado
                token_obj.is_used = True
                token_obj.save()
                
                return Response({
                    "message": "Contraseña actualizada exitosamente."
                }, status=status.HTTP_200_OK)
                
            except PasswordResetToken.DoesNotExist:
                return Response({
                    "error": "Token inválido."
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@user_schema
@extend_schema(tags=['usuarios'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsOwnerUser]

    def get_serializer_class(self):
        """
        Usar diferentes serializers dependiendo de la acción
        """
        if self.action in ['update', 'partial_update']:
            return UserUpdateProfileSerializer
        return UserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=partial, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)