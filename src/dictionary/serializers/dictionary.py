from rest_framework import serializers

from dictionary.models import Dictionary
from dictionary.serializers.text import TextSerializer
from dictionary.serializers.token import TokenSerializer


class DictionarySerializer(serializers.HyperlinkedModelSerializer):
    tokens = TokenSerializer(many=True, read_only=True)
    texts = TextSerializer(many=True, read_only=True)

    class Meta:
        model = Dictionary
        fields = [
            'url',
            'id',
            'title',
            'creation_date',
            'description',

            'tokens',
            'texts',
        ]
