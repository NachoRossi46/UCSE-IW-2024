from rest_framework import serializers
from .models import User, Rol
from propiedades.models import Edificio
import re

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'rol']

class EdificioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edificio
        fields = ['id', 'nombre', 'direccion', 'numero', 'ciudad']

class UserSerializer(serializers.ModelSerializer):
    rol = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all(), write_only=True)
    rol_info = RolSerializer(source='rol', read_only=True)
    password = serializers.CharField(write_only=True, required=True)
    edificio = EdificioSerializer(read_only=True)
    edificio_id = serializers.PrimaryKeyRelatedField(queryset=Edificio.objects.all(), write_only=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'nombre', 'apellido', 'rol', 'rol_info', 'is_active', 'is_staff', 'password', 'edificio', 'edificio_id', 'piso', 'numero']
        read_only_fields = ['is_active', 'is_staff']
        
    def validate_piso(self, value):
        # Valido que el piso esté entre 1 y 49
        if value is not None and (value < 1 or value > 49):
            raise serializers.ValidationError("El piso debe estar entre 1 y 49.")
        return value
    
    def validate_numero(self, value):
        # Valido que el número sea exactamente una letra
        if value is not None:
            if not re.match(r'^[A-Za-z]$', value):
                raise serializers.ValidationError("El número debe ser exactamente una letra (ej: A, B, C).")
        return value
    
    def validate_rol(self, value):
        if value.rol == 'Administrador':
            user = self.context['request'].user
            if not user.is_authenticated or not user.is_superuser:
                raise serializers.ValidationError("Solo los superusuarios pueden seleccionar el rol de Administrador.")
        return value

    def create(self, validated_data):
        edificio_id = validated_data.pop('edificio_id', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        if edificio_id:
            user.edificio = edificio_id
        user.save()
        return user

    def update(self, instance, validated_data):
        edificio_id = validated_data.pop('edificio_id', None)
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if edificio_id:
            instance.edificio = edificio_id
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    rol = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.exclude(rol='Administrador'), required=True)
    edificio = serializers.PrimaryKeyRelatedField(queryset=Edificio.objects.all(), required=True)
    piso = serializers.IntegerField(required=False, allow_null=True)
    numero = serializers.CharField(max_length=10, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['email', 'nombre', 'apellido', 'password', 'rol', 'edificio', 'piso', 'numero']
        
    def validate_piso(self, value):
        # Valido que el piso esté entre 1 y 49
        if value is not None and (value < 1 or value > 49):
            raise serializers.ValidationError("El piso debe estar entre 1 y 49.")
        return value
    
    def validate_numero(self, value):
        # Valido que el número sea exactamente una letra
        if value is not None:
            if not re.match(r'^[A-Za-z]$', value):
                raise serializers.ValidationError("El número debe ser exactamente una letra (ej: A, B, C).")
        return value

    def validate(self, attrs):
        piso = attrs.get('piso')
        numero = attrs.get('numero')

        if (piso is None and numero is not None) or (piso is not None and numero is None):
            raise serializers.ValidationError("Debe proporcionar tanto el piso como el número, o ninguno de los dos.")

        return attrs


    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            apellido=validated_data['apellido'],
            password=validated_data['password'],
            rol=validated_data['rol'],
            edificio=validated_data['edificio'],
            piso=validated_data.get('piso'),
            numero=validated_data.get('numero'),
            is_active=False,
            is_staff=False
        )
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)
    
class UserUpdateProfileSerializer(serializers.ModelSerializer):
    rol_info = RolSerializer(source='rol', read_only=True)
    edificio = EdificioSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'nombre', 'apellido',  # Campos editables
            'rol_info', 'edificio', 'piso', 'numero', 'is_active', 'is_staff'  # Campos de solo lectura
        ]
        read_only_fields = ['id', 'rol_info', 'edificio', 'piso', 'numero', 'is_active', 'is_staff']

    def validate_email(self, value):
        # Validar que el email sea único, excluyendo el usuario actual
        user = self.context['request'].user
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Este email ya está en uso.")
        return value