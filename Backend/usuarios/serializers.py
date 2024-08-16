from rest_framework import serializers
from .models import User, Rol

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'rol']

class UserSerializer(serializers.ModelSerializer):
    rol = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all(), write_only=True)
    rol_info = RolSerializer(source='rol', read_only=True)
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'nombre', 'apellido', 'rol', 'rol_info', 'is_active', 'is_staff', 'password']
        read_only_fields = ['is_active', 'is_staff']

    def validate_rol(self, value):
        if value.rol == 'Administrador':
            user = self.context['request'].user
            if not user.is_authenticated or not user.is_superuser:
                raise serializers.ValidationError("Solo los superusuarios pueden seleccionar el rol de Administrador.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    rol = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.exclude(rol='Administrador'), required=True)

    class Meta:
        model = User
        fields = ['email', 'nombre', 'apellido', 'password', 'rol']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            apellido=validated_data['apellido'],
            password=validated_data['password'],
            rol=validated_data['rol'],
            is_active=False,
            is_staff=False
        )
        return user





