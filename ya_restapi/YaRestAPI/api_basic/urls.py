from django.urls import path
from .views import ArticleAPIView, ArticleDetailAPIView
# from .views import article_list, article_detail,

urlpatterns = [
    # path('article/', article_list),
    path('article/', ArticleAPIView.as_view()),

    # path('article-detail/<int:pk>', article_detail),
    path('article-detail/<int:id>', ArticleDetailAPIView.as_view()),
]
