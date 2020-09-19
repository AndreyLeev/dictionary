from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from dictionary.models import Dictionary


class DictionarySerializer(serializers.HyperlinkedModelSerializer):
    tokens = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='token-detail',
        parent_lookup_kwargs={'dictionary_pk': 'dictionary__pk'}
    )
    texts = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='text-detail',
        parent_lookup_kwargs={'dictionary_pk': 'dictionary__pk'}
    )

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
