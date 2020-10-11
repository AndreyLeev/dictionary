from django.db import IntegrityError, transaction
from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from dictionary.models import Token, Dictionary
from dictionary.serializers.text import TextSerializer
from dictionary.serializers.token import TokenSerializer
from dictionary.utils.text import TextManager


class TokenErrors:
    TOKEN_ALREADY_EXISTS = "Word already exists."
    INVALID_QUERY_PARAM = "Invalid query parameters"


class TokenViewSet(viewsets.ModelViewSet, TextManager):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = (
        'label',
        'frequency',
    )
    search_fields = (
        'label',
        'frequency',
    )
    ordering_fields = (
        'label',
        'frequency',
    )

    def get_queryset(self):
        return Token.objects.filter(dictionary=self.kwargs['dictionary_pk'])

    def perform_create(self, serializer):
        dictionary_pk = self.kwargs.get('dictionary_pk')
        try:
            serializer.save(dictionary_id=dictionary_pk)
        except IntegrityError:
            raise ValidationError(
                detail=TokenErrors.TOKEN_ALREADY_EXISTS,
                code=400,
            )

    def perform_update(self, serializer):
        old_token_obj: Token = self.get_object()
        new_instance: Token = serializer.save(
            dictionary_id=self.kwargs.get('dictionary_pk'),
        )

        texts = self.get_token_related_text_objects(
            dictionary=new_instance.dictionary,
            token=old_token_obj.label,
        )
        with transaction.atomic():
            for text_obj in texts:
                old_token = old_token_obj.label
                new_token = new_instance.label
                text_obj.text = self.replace_token(
                    text=text_obj.text,
                    old_token=old_token,
                    new_token=new_token,
                )
                text_obj.token_statistics[new_token] = text_obj.token_statistics.pop(old_token)
                text_obj.save()

    def perform_destroy(self, instance: Token):
        texts = self.get_token_related_text_objects(
            dictionary=instance.dictionary,
            token=instance.label,
        )

        with transaction.atomic():
            for text_obj in texts:
                text_obj.text = self.delete_token(
                    text=text_obj.text,
                    token=instance.label,
                )
                text_obj.token_statistics.pop(instance.label)
                text_obj.save()

        instance.delete()


class TokenTextsListView(APIView, TextManager):
    """
    View to list all texts with required token.

    url example: texts/?dict_id=2&token=foo
    """

    def get(self, request):
        token = request.GET.get('token')
        dict_id = request.GET.get('dict_id')

        if not (token and dict_id):
            raise ValidationError(
                detail=TokenErrors.INVALID_QUERY_PARAM,
                code=400,
            )

        texts = self.get_token_related_text_objects(
            dictionary=Dictionary.objects.get(id=dict_id),
            token=token,
        )
        serialized_texts = [TextSerializer(text).data for text in texts]

        return Response(data=serialized_texts)
