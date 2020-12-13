from abc import ABC, abstractmethod


class BaseLemmaManager(ABC):

    @classmethod
    @abstractmethod
    def get_lemma_from_token(
            cls,
            token: str
    ) -> str:
        pass
