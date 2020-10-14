from rest_framework import serializers

from dictionary.models import Dictionary


class DictionarySerializer(serializers.HyperlinkedModelSerializer):
    total_unique_tokens = serializers.IntegerField(read_only=True)
    total_tokens = serializers.IntegerField(read_only=True)
    # TODO add text count field
    class Meta:
        model = Dictionary
        fields = [
            'url',
            'id',
            'title',
            'creation_date',
            'description',

            'total_unique_tokens',
            'total_tokens',
        ]
