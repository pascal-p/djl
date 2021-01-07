from django.urls import path
from .views import ArticleAPIView, ArticleDetailAPIView, GenericAPIView

urlpatterns = [
    path('article/', ArticleAPIView.as_view()),

    path('article-detail/<int:id>', ArticleDetailAPIView.as_view()),

    path('generic/article/<int:id>', GenericAPIView.as_view()),
]
