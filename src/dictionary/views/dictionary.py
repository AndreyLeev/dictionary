from rest_framework import viewsets

from dictionary.models import Dictionary
from dictionary.serializers.dictionary import DictionarySerializer


class DictionaryViewSet(viewsets.ModelViewSet):
    queryset = Dictionary.objects.all()
    serializer_class = DictionarySerializer
