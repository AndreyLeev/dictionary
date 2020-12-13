from django.db.models import Sum
from rest_framework import serializers

from dictionary.models import Tag


class TagSerializer(serializers.ModelSerializer):
    frequency = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = [
            'id',
            'code',
            'title',
            'examples',
            'frequency',
        ]

    def get_frequency(self, instance):
        tag = Tag.objects.filter(id=instance.id).annotate(frequency=Sum('tokens__frequency'))[0]
        return tag.frequency or 0
