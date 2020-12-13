import string
import logging
import itertools
from collections import defaultdict
from typing import Dict

from django.db.models import F
from dictionary.models import Token, Text, Tag
from django.db import transaction

from dictionary.utils.managers.managers import ParsingManagersMixin

logger = logging.getLogger(__name__)


class DictionaryManagementMixin(ParsingManagersMixin):

    class Errors:
        TOKEN_IS_NOT_ALPHABETIC = "Not all the characters in the word are alphabetic"

    @classmethod
    def create_dict_from_text(cls, text: str) -> Dict[str, int]:
        tokenize_manager = cls.get_tokenize_manager()

        dictionary = defaultdict(lambda: 0)
        for token in tokenize_manager.tokenize_text(text):
            cleaned_token = cls.serialize_token(token)

            try:
                cls.validate_token(cleaned_token)
            except ValueError:
                # just skip broken word
                logger.debug(f'Invalid token: {cleaned_token}')
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


class TokenDictionaryDAL(DictionaryManagementMixin, ParsingManagersMixin):

    @classmethod
    def _update_tokens_tags_relations(
            cls,
            token_obj: Token,
            tagged_words_dict: dict,
    ) -> None:
        # TODO: find a better solution to update tags of word
        #  without performing many extra DB queries
        new_tags_titles = tagged_words_dict.get(token_obj.label, [])
        existing_tags_titles = token_obj.tags.values_list('title', flat=True) or []
        current_tags_titles = {*new_tags_titles, *existing_tags_titles}
        current_tags = Tag.objects.filter(code__in=current_tags_titles)
        token_obj.tags.clear()
        token_obj.tags.add(*current_tags)

    @classmethod
    def create_tokens_dictionary_relations(
            cls,
            text_obj: Text,
    ) -> None:
        tagging_manager = cls.get_tagging_manager()
        tagged_words_dict = tagging_manager.get_tags_dict_from_text(text_obj.text)

        new_dictionary_objects = cls.create_dict_from_text(text_obj.text)
        text_obj.token_statistics = new_dictionary_objects
        text_obj.save()

        lemma_manager = cls.get_lemma_manager()

        with transaction.atomic():
            for label, frequency in new_dictionary_objects.items():

                lemma = lemma_manager.get_lemma_from_token(label)

                token_obj, is_created_flag = Token.objects.get_or_create(
                    dictionary=text_obj.dictionary,
                    label=label,
                    lemma=lemma
                )

                cls._update_tokens_tags_relations(
                    token_obj=token_obj,
                    tagged_words_dict=tagged_words_dict,
                )

                token_obj.frequency = F('frequency') + frequency
                token_obj.save()

    @classmethod
    def update_tokens_dictionary_relations(
            cls,
            text_obj: Text,
    ) -> None:
        tagging_manager = cls.get_tagging_manager()
        tagged_words_dict = tagging_manager.get_tags_dict_from_text(text_obj.text)

        new_dict = cls.create_dict_from_text(text_obj.text)
        old_dict = text_obj.token_statistics
        diff_dict = cls.get_dict_diff(old_dict, new_dict)

        text_obj.token_statistics = new_dict
        text_obj.save()

        lemma_manager = cls.get_lemma_manager()

        with transaction.atomic():
            for label, frequency_diff in diff_dict.items():

                lemma = lemma_manager.get_lemma_from_token(label)

                token_obj, is_created_flag = Token.objects.get_or_create(
                    dictionary=text_obj.dictionary,
                    label=label,
                    lemma=lemma,
                )
                cls._update_tokens_tags_relations(
                    token_obj=token_obj,
                    tagged_words_dict=tagged_words_dict,
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
