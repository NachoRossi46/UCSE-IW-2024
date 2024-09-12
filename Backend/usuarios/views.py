from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer



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



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]






