from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ArticleAPIView, ArticleDetailAPIView, \
  GenericAPIView, ArticleViewSet

router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')


urlpatterns = [
    # ArticleViewSet
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>', include(router.urls)),

    # APIView
    path('article/', ArticleAPIView.as_view()),
    path('article-detail/<int:id>', ArticleDetailAPIView.as_view()),

    # GenericAPIView
    path('generic/article/<int:id>', GenericAPIView.as_view()),
]
