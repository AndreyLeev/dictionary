from typing import List

import nltk

from dictionary.utils.managers.tokenize.common import BaseTokenizeManager


class NLTKTokenizeManager(BaseTokenizeManager):

    @classmethod
    def tokenize_text(
            cls,
            plain_text: str
    ) -> List[str]:
        return nltk.word_tokenize(plain_text)
