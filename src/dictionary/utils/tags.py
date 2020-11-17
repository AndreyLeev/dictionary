from typing import Optional, Dict

import nltk


class TaggedTextManager:

    @classmethod
    def get_tagged_text(
            cls,
            text: str,
            tagged_words_dict: Optional[Dict] = None,
    ) -> str:
        from dictionary.utils.dictionary import DictionaryManagementMixin
        new_dict = DictionaryManagementMixin.create_dict_from_text(text)

        if not tagged_words_dict:
            tagged_words_dict = dict(nltk.pos_tag(new_dict.keys()))
        return " ".join(
            [
                f"{word}__{tagged_words_dict[word]}"
                for word in nltk.word_tokenize(text)
                if tagged_words_dict.get(word)
            ]
        )

    @classmethod
    def get_tag_dict_from_tagged_text(
            cls,
            tagged_text: str
    ) -> Dict:
        return dict(
            [
                tag_and_token.split("__")
                for tag_and_token in tagged_text.split()
            ]
        )

    @classmethod
    def get_plain_text_from_tagged_text(
            cls,
            tagged_text: str
    ) -> str:
        return " ".join(
            [
                tag_and_token.split("__")[0]
                for tag_and_token in tagged_text.split()
            ]
        )
