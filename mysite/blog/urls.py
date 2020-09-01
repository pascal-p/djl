from django.urls import path

from . import views
from django.views.generic import TemplateView
from .feeds import LatestPostsFeed


app_name = 'blog'
urlpatterns = [
    # post views

    # R
    path('', views.PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='post_list_by_tag'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.PostDetailView.as_view(), name='post_detail'),

    # CUD
    # path('create/', views.PostCreate.as_view(), name='post_create'),
    # path('<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
    # path('<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),

    # sharing post via email functionality using FBV
    path('<int:post_id>/share/', views.post_share, name='post_share'),

    # Feeds
    path('feed/', LatestPostsFeed(), name='post_feed'),
]
