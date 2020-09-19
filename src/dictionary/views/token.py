from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from dictionary.models import Token
from dictionary.serializers.token import TokenSerializer


class TokenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = (
        'label',
        'frequency',
    )
    search_fields = (
        'label',
        'frequency',
    )
    ordering_fields = (
        'label',
        'frequency',
    )

    def get_queryset(self):
        return Token.objects.filter(dictionary=self.kwargs['dictionary_pk'])
