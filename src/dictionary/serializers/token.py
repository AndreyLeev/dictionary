from rest_framework import serializers

from dictionary.models import Token


class TokenSerializer(serializers.ModelSerializer):
    dictionary = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Token
        fields = [
            'id',
            'label',
            'frequency',

            'dictionary',
        ]
