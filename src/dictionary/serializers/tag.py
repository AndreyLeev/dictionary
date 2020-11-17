from rest_framework import serializers

from dictionary.models import Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = [
            'id',
            'code',
            'title',
            'examples',
        ]
