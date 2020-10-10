from rest_framework import serializers

from dictionary.models import Text, Dictionary


class TextSerializer(serializers.ModelSerializer):
    dictionary = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Text
        fields = [
            'id',
            'text',
            'title',
            'creation_date',
            'token_statistics',

            'dictionary',
        ]
        read_only_fields = (
            'token_statistics',
        )

    def create(self, validated_data):
        dictionary_id = validated_data.pop('dictionary_id')
        dictionary = Dictionary.objects.get(id=dictionary_id)  # TODO raise 404
        text = Text.objects.create(dictionary=dictionary, **validated_data)
        return text
