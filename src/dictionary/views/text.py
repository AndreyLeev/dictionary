from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from dictionary.models import Text, Dictionary
from dictionary.serializers.text import TextSerializer
from dictionary.utils.dictionary import TokenDictionaryDAL
from dictionary.utils.managers.managers import ParsingManagersMixin


class TextViewSet(viewsets.ModelViewSet, TokenDictionaryDAL, ParsingManagersMixin):
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

    def _process_tagged_and_plain_text(self, validated_data: dict) -> (str, str):
        tagging_manager = self.get_tagging_manager()

        is_tagged_text_updated = validated_data.get('is_tagged_text')
        if is_tagged_text_updated:
            tagged_text = validated_data.get('tagged_text')
            text = tagging_manager.get_plain_text_from_tagged_text(tagged_text)
        else:
            text = validated_data.get('text')
            tagged_text = tagging_manager.get_tagged_text_from_plain_text(text)

        return text, tagged_text

    def perform_create(self, serializer: TextSerializer):
        text, tagged_text = self._process_tagged_and_plain_text(serializer.validated_data)

        instance = serializer.save(
            dictionary_id=self.kwargs.get('dictionary_pk'),
            text=text,
            tagged_text=tagged_text,
        )
        self.create_tokens_dictionary_relations(text_obj=instance)

    def perform_update(self, serializer):
        dictionary_pk = self.kwargs.get('dictionary_pk')
        text, tagged_text = self._process_tagged_and_plain_text(serializer.validated_data)

        instance: Text = serializer.save(
            dictionary_id=dictionary_pk,
            text=text,
            tagged_text=tagged_text,
        )

        self.update_tokens_dictionary_relations(text_obj=instance)

    def perform_destroy(self, instance: Text):
        self.delete_tokens_dictionary_relations(
            dictionary=instance.dictionary,
            old_text=instance.text,
        )
        instance.delete()


class TextFileUploaderView(APIView, TokenDictionaryDAL):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        uploaded_file = request.data.get('file')
        text_obj = Text.objects.create(
            text=uploaded_file.read().decode(),
            title=uploaded_file.name,
            dictionary=Dictionary.objects.get(pk=kwargs.get('dict_id'))
        )
        self.create_tokens_dictionary_relations(text_obj)
        return Response()
