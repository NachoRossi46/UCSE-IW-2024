import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoPrincipal.settings')
django.setup()

from usuarios.models import Rol
from comunicaciones.models import TipoPosteo
from servicios.models import TipoServicio

def initialize_database():

    roles = ['Administrador', 'Colaborador', 'Inquilino', 'Duenio']
    for rol_name in roles:
        Rol.objects.get_or_create(rol=rol_name)
    print("Roles creados o verificados con éxito.")

    tipo_posteos = ['Aviso', 'Consulta', 'Reclamo']
    for tipo_name in tipo_posteos:
        TipoPosteo.objects.get_or_create(tipo=tipo_name)
    print("Tipos de posteos creados o verificados con éxito.")

    tipo_servicios = ['Plomería', 'Gasista', 'Electricista', 'Técnico en Refrigeración', 'Cerrajero', 'Pintor']
    for tipo_name in tipo_servicios:
        TipoServicio.objects.get_or_create(tipo=tipo_name)
    print("Tipos de servicios creados o verificados con éxito.")

if __name__ == '__main__':
    initialize_database()
