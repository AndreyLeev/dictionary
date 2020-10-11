import re
from typing import List

from dictionary.models import Text, Dictionary


class TextManager:

    # \b - word boundaries
    # flags=re.I - ignore case

    @classmethod
    def replace_token(cls, text: str, new_token: str, old_token: str) -> str:
        return re.sub(r'\b' + old_token + r'\b', new_token, text, flags=re.I)

    @classmethod
    def delete_token(cls, text: str, token: str) -> str:
        return re.sub(r'\b' + token + r'\b', '', text, flags=re.I)

    @classmethod
    def get_token_related_text_objects(cls, dictionary: Dictionary, token: str) -> List[Text]:
        return Text.objects.filter(
            dictionary=dictionary,
            token_statistics__has_key=token
        )
