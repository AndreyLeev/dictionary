from rest_framework import serializers

from dictionary.models import Token, Dictionary


class TokenSerializer(serializers.ModelSerializer):
    dictionary = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = serializers.SerializerMethodField(
        '_tags',
        read_only=True,
    )

    lemma = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Token
        fields = [
            'id',
            'label',
            'frequency',
            'tags',
            'lemma',
            'dictionary',
        ]
        read_only_fields = (
            'frequency',
        )

    def create(self, validated_data):
        dictionary_id = validated_data.pop('dictionary_id')
        dictionary = Dictionary.objects.get(id=dictionary_id)  # TODO raise 404
        token = Token.objects.create(dictionary=dictionary, **validated_data)
        return token

    def _tags(self, obj):
        tags = ", ".join([tag.code for tag in obj.tags.all()])
        if not tags:    # TODO delete ME
            tags = 'NN'
        return tags
