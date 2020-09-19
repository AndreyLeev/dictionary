from typing import Dict

from django.db.models import F
from rest_framework import viewsets

from dictionary.models import Text, Token, Dictionary
from dictionary.serializers.text import TextSerializer
from dictionary.utils.dictionary import DictionaryCreationMixin


class TextViewSet(viewsets.ModelViewSet, DictionaryCreationMixin):
    queryset = Text.objects.all()
    serializer_class = TextSerializer

    def get_queryset(self):
        return Text.objects.filter(dictionary=self.kwargs['dictionary_pk'])

    def perform_create(self, serializer):
        dictionary_pk = self.kwargs.get('dictionary_pk')
        instance = serializer.save(dictionary_id=dictionary_pk)

        parsed_dictionary = self.create_dict_from_text(instance.text)
        self.create_tokens_dictionary_relations(
            dictionary_pk=dictionary_pk,
            new_dictionary_objects=parsed_dictionary,
        )

    @classmethod
    def create_tokens_dictionary_relations(
            cls,
            dictionary_pk,
            new_dictionary_objects: Dict[str, int]
    ) -> None:
        for label, frequency in new_dictionary_objects.items():
            token_obj, is_created_flag = Token.objects.get_or_create(
                dictionary=Dictionary.objects.get(id=dictionary_pk),
                label=label,
            )
            token_obj.frequency = F('frequency') + frequency
            token_obj.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        #TODO
