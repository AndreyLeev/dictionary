from collections import defaultdict
from typing import Dict, List

import nltk

from dictionary.utils.constants import TaggedTextTagsWordsDelimiter
from dictionary.utils.managers.tagging.common import BaseTaggingManager


class NLTKTaggingManager(BaseTaggingManager):

    DEFAULT_DELIMITER = TaggedTextTagsWordsDelimiter.SINGLE_UNDERSCORE

    @classmethod
    def get_delimiter(cls) -> str:
        return cls.DEFAULT_DELIMITER

    @classmethod
    def get_tags_dict_from_text(
            cls,
            plain_text: str
    ) -> Dict[str, List[str]]:
        tagged_text = nltk.pos_tag(nltk.word_tokenize(plain_text))
        # tagged_text example: [('At', 'IN'), ('eight', 'CD'), ('At', 'JJ')]

        tags_dict = defaultdict(list)
        for word, tag in tagged_text:
            tags_dict[word].append(tag)

        return tags_dict

    @classmethod
    def get_tagged_text_from_plain_text(
            cls,
            plain_text: str
    ) -> str:
        delimiter = cls.get_delimiter()

        tagged_text = nltk.pos_tag(nltk.word_tokenize(plain_text))
        # tagged_text example: [('At', 'IN'), ('eight', 'CD'), ('At', 'JJ')]

        return " ".join(
            [
                f"{word}{delimiter}{tag}"
                for word, tag in tagged_text
            ]
        )

    @classmethod
    def get_plain_text_from_tagged_text(
            cls,
            tagged_text: str
    ) -> str:
        delimiter = cls.get_delimiter()

        return " ".join(
            [
                word_w_tag.split(delimiter)[0]
                for word_w_tag in tagged_text.split()
            ]
        )

    @classmethod
    def tags_dict_from_tagged_text(
            cls,
            tagged_text: str
    ) -> Dict[str, List[str]]:
        delimiter = cls.get_delimiter()

        tags_dict = defaultdict(list)
        for word_w_tag in tagged_text.split():
            word, tag = word_w_tag.split(delimiter)
            tags_dict[word].append(tag)

        return tags_dict
