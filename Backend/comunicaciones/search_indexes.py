from haystack import indexes
from .models import Posteo

class PosteoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='titulo')
    descripcion = indexes.CharField(model_attr='descripcion')

    def get_model(self):
        return Posteo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()