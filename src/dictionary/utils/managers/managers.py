from dictionary.utils.constants import TaggingManagerType, TokenizeManagerType
from dictionary.utils.managers.tagging.nltk_tagging import NLTKTaggingManager
from dictionary.utils.managers.tokenize.nltk_tokenize import NLTKTokenizeManager


class ParsingManagersMixin:

    _tagging_managers_registry = {
        TaggingManagerType.NLTK: NLTKTaggingManager
    }

    _tokenize_managers_registry = {
        TokenizeManagerType.NLTK: NLTKTokenizeManager
    }

    @classmethod
    def get_tagging_manager(cls):
        return cls._tagging_managers_registry.get(TaggingManagerType.NLTK)

    @classmethod
    def get_tokenize_manager(cls):
        return cls._tokenize_managers_registry.get(TokenizeManagerType.NLTK)
