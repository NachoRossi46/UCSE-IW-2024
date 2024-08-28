from rest_framework import viewsets
from .models import Edificio
from .serializers import EdificioSerializer

class EdificioViewSet(viewsets.ModelViewSet):
    queryset = Edificio.objects.all()
    serializer_class = EdificioSerializer


