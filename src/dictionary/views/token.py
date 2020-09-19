from rest_framework import viewsets

from dictionary.models import Token
from dictionary.serializers.token import TokenSerializer


class TokenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

    def get_queryset(self):
        return Token.objects.filter(dictionary=self.kwargs['dictionary_pk'])
