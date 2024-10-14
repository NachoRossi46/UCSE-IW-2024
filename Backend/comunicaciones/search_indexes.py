from haystack import indexes
from .models import Posteo

class PosteoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='titulo')
    descripcion = indexes.CharField(model_attr='descripcion')
    edificio = indexes.IntegerField(null=True)

    def get_model(self):
        return Posteo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
    
    def prepare_edificio(self, obj):
        if obj.usuario and obj.usuario.edificio:
            return obj.usuario.edificio.id
        return None  # Retorna None si no hay edificio

    def prepare(self, obj):
        data = super(PosteoIndex, self).prepare(obj)
        return data

