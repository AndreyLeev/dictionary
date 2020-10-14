import string
import logging
import itertools
from collections import defaultdict
from typing import Dict

from django.db.models import F
from dictionary.models import Token, Text
from django.db import transaction

logger = logging.getLogger(__name__)


class DictionaryManagementMixin:

    class Errors:
        TOKEN_IS_NOT_ALPHABETIC = "Not all the characters in the word are alphabetic"

    @classmethod
    def create_dict_from_text(cls, text: str) -> Dict[str, int]:
        dictionary = defaultdict(lambda: 0)

        for token in text.split():
            cleaned_token = cls.serialize_token(token)

            try:
                cls.validate_token(cleaned_token)
            except ValueError:
                # just skip broken word
                continue

            dictionary[cleaned_token] += 1

        logger.debug(f"Parsed token dictionary from text dict={dict(dictionary)}")
        return dictionary

    @classmethod
    def get_dict_diff(
            cls,
            old_dict: Dict[str, int],
            new_dict: Dict[str, int]
    ) -> Dict[str, int]:

        diff_dict = {}
        for label in itertools.chain(new_dict.keys(), old_dict.keys()):
            diff = new_dict.get(label, 0) - old_dict.get(label, 0)
            if diff:
                diff_dict[label] = diff

        logger.debug(f"Parsed token diff dictionary dict={diff_dict}")
        return diff_dict

    @classmethod
    def validate_token(cls, token: str) -> str:

        # Check if all the characters in the text are letters
        if not token.isalpha():
            raise ValueError(cls.Errors.TOKEN_IS_NOT_ALPHABETIC)

        return token

    @classmethod
    def serialize_token(cls, token: str) -> str:
        token = token.strip(string.punctuation)
        token = token.lower()
        return token


class TokenDictionaryDAL(DictionaryManagementMixin):

    @classmethod
    def create_tokens_dictionary_relations(
            cls,
            text_obj: Text,
    ) -> None:
        new_dictionary_objects = cls.create_dict_from_text(text_obj.text)

        text_obj.token_statistics = new_dictionary_objects
        text_obj.save()

        with transaction.atomic():
            for label, frequency in new_dictionary_objects.items():
                token_obj, is_created_flag = Token.objects.get_or_create(
                    dictionary=text_obj.dictionary,
                    label=label,
                )
                token_obj.frequency = F('frequency') + frequency
                token_obj.save()

    @classmethod
    def update_tokens_dictionary_relations(
            cls,
            text_obj: Text,
    ) -> None:

        new_dict = cls.create_dict_from_text(text_obj.text)
        old_dict = text_obj.token_statistics
        diff_dict = cls.get_dict_diff(old_dict, new_dict)

        text_obj.token_statistics = new_dict
        text_obj.save()

        with transaction.atomic():
            for label, frequency_diff in diff_dict.items():
                token_obj, is_created_flag = Token.objects.get_or_create(
                    dictionary=text_obj.dictionary,
                    label=label,
                )
                token_obj.frequency += frequency_diff

                if not token_obj.frequency:
                    token_obj.delete()
                else:
                    token_obj.save()

    @classmethod
    def delete_tokens_dictionary_relations(
            cls,
            dictionary,
            old_text: str,
    ) -> None:
        old_dict = cls.create_dict_from_text(old_text)

        with transaction.atomic():
            for label, frequency in old_dict.items():
                token_obj = Token.objects.get(
                    dictionary=dictionary,
                    label=label,
                )
                token_obj.frequency -= frequency

                if not token_obj.frequency:
                    token_obj.delete()
                else:
                    token_obj.save()
