import nltk
from nltk.stem import WordNetLemmatizer

from dictionary.models import Lemma, Tag
from dictionary.utils.managers.lemma.common import BaseLemmaManager


class NLTKLemmaManager(BaseLemmaManager):

    @classmethod
    def get_lemma_from_token(
            cls,
            token: str
    ) -> Lemma:
        wnl = WordNetLemmatizer()
        lemma_label = wnl.lemmatize(token)

        # nltk_tags example: [('play', 'NN')]
        nltk_tags = nltk.pos_tag([lemma_label])
        tag_code = nltk_tags[0][1]

        tag_obj = Tag.objects.get(code=tag_code)

        lemma = Lemma(
            label=lemma_label,
            tag=tag_obj
        )
        lemma.save()

        return lemma
