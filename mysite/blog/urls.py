from django.urls import path

from . import views
from django.views.generic import TemplateView

app_name = 'blog'
urlpatterns = [
    # post views

    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.PostDetailView.as_view(), name='post_detail'),

]
