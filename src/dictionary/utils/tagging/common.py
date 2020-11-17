from abc import ABC, abstractmethod
from typing import Dict, List


class BaseTaggingManager(ABC):

    @classmethod
    @abstractmethod
    def get_tags_dict_from_text(
            cls,
            plain_text: str
    ) -> Dict[str, List[str]]:
        """
        Return mapping of words and tags in the next format:
        {
            'The': ['AT', 'RB'],
            'now': ['RB'],
            ...
        }

        !!! IMPORTANT: single word can has more than one tag
        """
        pass

    @classmethod
    @abstractmethod
    def get_tagged_text_from_plain_text(
            cls,
            plain_text: str
    ) -> str:
        """
        Return tagged text where every word has it's own tags set
        concatenated with special delimiter.

        Example of tagged text with double underscore delimiter:
        "The__AT__RB now__RB"

        !!! IMPORTANT: single word can has more than one tag
        """
        pass

    @classmethod
    @abstractmethod
    def get_plain_text_from_tagged_text(
            cls,
            tagged_text: str
    ) -> str:
        """
        Get rid of all word tags and returns plain text preserving words order

        Example:
        "The__AT__RB now__RB" --> "The now"
        """
        pass

    @classmethod
    @abstractmethod
    def tags_dict_from_tagged_text(
            cls,
            tagged_text: str
    ) -> Dict[str, List[str]]:
        """
        Parse tagged text and return mapping of words and tags in the next format:
        {
            'The': ['AT', 'RB'],
            'now': ['RB'],
            ...
        }
        """
        pass
