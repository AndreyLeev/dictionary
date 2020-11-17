from django.urls import re_path, include, path
from rest_framework_nested import routers

from dictionary.views.dictionary import DictionaryViewSet
from dictionary.views.tag import TagViewSet
from dictionary.views.text import TextViewSet, TextFileUploaderView
from dictionary.views.token import TokenViewSet, TokenTextsListView

router = routers.SimpleRouter()
router.register('dictionaries', DictionaryViewSet)
router.register('tags', TagViewSet)


dictionaries_router = routers.NestedSimpleRouter(
    router,
    'dictionaries',
    lookup='dictionary',
)
dictionaries_router.register('texts', TextViewSet)
dictionaries_router.register('tokens', TokenViewSet)


urlpatterns = [
    re_path('', include(router.urls)),
    re_path('', include(dictionaries_router.urls)),
    path('texts/', TokenTextsListView.as_view(), name='token-texts'),

    # TODO move under common /dictionaries endpoints
    path('dict/<int:dict_id>/texts/upload/', TextFileUploaderView.as_view(), name='upload-file'),
]
