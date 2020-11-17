from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from dictionary.models import Tag
from dictionary.serializers.tag import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
