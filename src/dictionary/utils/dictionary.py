import string
import logging
from collections import defaultdict
from typing import Dict, Optional


logger = logging.getLogger(__name__)

class DictionaryCreationMixin:

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

