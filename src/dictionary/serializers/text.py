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
    is_tagged_text = serializers.BooleanField(
        required=False,
        default=False,
        write_only=True,
        help_text=(
            "Specifies which approach was chosen "
            "for updating the text (tagged or plain text)"
        ),
    )

    class Meta:
        model = Text
        fields = [
            'id',
            'text',
            'tagged_text',
            'title',
            'creation_date',

            'total_unique_tokens',
            'total_tokens',
            'is_tagged_text',

            'dictionary',
        ]
        extra_kwargs = {
            'text': {'required': False},
            'tagged_text': {'required': False},
        }

    def _total_unique_tokens(self, obj):
        return len(obj.token_statistics)

    def _total_tokens(self, obj):
        return sum(obj.token_statistics.values())

    def create(self, validated_data):
        # not a model field
        validated_data.pop('is_tagged_text', None)

        dictionary_id = validated_data.pop('dictionary_id')
        dictionary = Dictionary.objects.get(id=dictionary_id)  # TODO raise 404
        text = Text.objects.create(dictionary=dictionary, **validated_data)
        return text


class TokenTextsSerializer(serializers.Serializer):
    text_id = serializers.IntegerField()
    text_title = serializers.CharField(max_length=255)
    token_total = serializers.IntegerField()
