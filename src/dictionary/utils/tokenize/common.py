from abc import ABC, abstractmethod
from typing import List


class BaseTokenizeManager(ABC):

    @classmethod
    @abstractmethod
    def tokenize_text(
            cls,
            plain_text: str
    ) -> List[str]:
        pass
