from collections import defaultdict

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from dictionary.models import Tag, Text
from dictionary.serializers.tag import TagSerializer, TagWordSerializer, TagTagSerializer
from dictionary.utils.managers.managers import ParsingManagersMixin


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]


class TagWordViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagWordSerializer

    def get_queryset(self):
        res = []

        for tag in Tag.objects.all():
            for token in tag.tokens.filter(dictionary=self.kwargs['dictionary_pk']).all():
                res.append(
                    {
                        'code': tag.code,
                        'word': token.label,
                        'frequency': token.frequency,
                    }
                )

        return res


class TagTagViewSet(viewsets.ModelViewSet, ParsingManagersMixin):
    queryset = Tag.objects.all()
    serializer_class = TagTagSerializer

    def get_queryset(self):
        tagging_manager = self.get_tagging_manager()

        tags_pair_statistic = defaultdict(lambda: 0)
        for text in Text.objects.filter(dictionary=self.kwargs['dictionary_pk']).all():
            for tags_pair in tagging_manager.get_tags_pair_from_tagged_text(text.tagged_text):
                tags_pair_statistic[tags_pair] += 1

        res = [
            {
                'code_1': key[0],
                'code_2': key[1],
                'frequency': value,
            }
            for key, value in tags_pair_statistic.items()
        ]

        return res
