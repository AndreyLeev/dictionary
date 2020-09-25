from django.db.models import Count, Sum
from rest_framework import viewsets

from dictionary.models import Dictionary
from dictionary.serializers.dictionary import DictionarySerializer


class DictionaryViewSet(viewsets.ModelViewSet):
    queryset = Dictionary.objects.all()
    serializer_class = DictionarySerializer

    def get_queryset(self):
        return Dictionary.objects.annotate(
            total_unique_tokens=Count('tokens'),
            total_tokens=Sum('tokens__frequency')
        )
