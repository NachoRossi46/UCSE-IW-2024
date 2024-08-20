import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoPrincipal.settings')
django.setup()

from usuarios.models import Rol

def initialize_database():
    # Crear roles
    roles = ['Administrador', 'Colaborador', 'Inquilino', 'Duenio']
    for rol_name in roles:
        Rol.objects.get_or_create(rol=rol_name)
    print("Roles creados o verificados con éxito.")

if __name__ == '__main__':
    initialize_database()
