from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from dictionary.models import Text
from dictionary.serializers.text import TextSerializer
from dictionary.utils.dictionary import TokenDictionaryDAL


class TextViewSet(viewsets.ModelViewSet, TokenDictionaryDAL):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = (
        'creation_date',
        'title',
        'text'
    )
    search_fields = (
        'title',
        'text',
    )
    ordering_fields = (
        'creation_date',
        'title',
    )

    def get_queryset(self):
        return Text.objects.filter(dictionary=self.kwargs['dictionary_pk'])

    def perform_create(self, serializer):
        dictionary_pk = self.kwargs.get('dictionary_pk')
        instance = serializer.save(dictionary_id=dictionary_pk)
        self.create_tokens_dictionary_relations(text_obj=instance)

    def perform_update(self, serializer):
        dictionary_pk = self.kwargs.get('dictionary_pk')
        text_obj: Text = self.get_object()

        instance: Text = serializer.save(dictionary_id=dictionary_pk)

        self.update_tokens_dictionary_relations(
            old_text=text_obj.text,
            text_obj=instance
        )

    def perform_destroy(self, instance: Text):
        self.delete_tokens_dictionary_relations(
            dictionary=instance.dictionary,
            old_text=instance.text,
        )
        instance.delete()
