from dictionary.utils.constants import (
    TaggingManagerType,
    TokenizeManagerType,
    LemmaManagerType,
)
from dictionary.utils.managers.lemma.nltk_lemma import NLTKLemmaManager
from dictionary.utils.managers.tagging.nltk_tagging import NLTKTaggingManager
from dictionary.utils.managers.tokenize.nltk_tokenize import NLTKTokenizeManager


class ParsingManagersMixin:

    _tagging_managers_registry = {
        TaggingManagerType.NLTK: NLTKTaggingManager
    }

    _tokenize_managers_registry = {
        TokenizeManagerType.NLTK: NLTKTokenizeManager
    }

    _lemma_managers_registry = {
        LemmaManagerType.NLTK: NLTKLemmaManager
    }

    @classmethod
    def get_tagging_manager(cls):
        return cls._tagging_managers_registry.get(TaggingManagerType.NLTK)

    @classmethod
    def get_tokenize_manager(cls):
        return cls._tokenize_managers_registry.get(TokenizeManagerType.NLTK)

    @classmethod
    def get_lemma_manager(cls):
        return cls._lemma_managers_registry.get(LemmaManagerType.NLTK)
