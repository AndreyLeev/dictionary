from rest_framework import serializers

from dictionary.models import Text, Dictionary


class TextSerializer(serializers.ModelSerializer):
    dictionary = serializers.PrimaryKeyRelatedField(read_only=True)
    total_tokens = serializers.SerializerMethodField(
        '_total_tokens',
        read_only=True,
    )
    total_unique_tokens = serializers.SerializerMethodField(
        '_total_unique_tokens',
        read_only=True,
    )

    class Meta:
        model = Text
        fields = [
            'id',
            'text',
            'title',
            'creation_date',

            'total_unique_tokens',
            'total_tokens',

            'dictionary',
        ]

    def _total_unique_tokens(self, obj):
        return len(obj.token_statistics)

    def _total_tokens(self, obj):
        return sum(obj.token_statistics.values())

    def create(self, validated_data):
        dictionary_id = validated_data.pop('dictionary_id')
        dictionary = Dictionary.objects.get(id=dictionary_id)  # TODO raise 404
        text = Text.objects.create(dictionary=dictionary, **validated_data)
        return text
