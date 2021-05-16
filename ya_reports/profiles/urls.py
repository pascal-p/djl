from django.urls import path
from .views import ya_profile_view

app_name = 'profiles'

urlpatterns = [
    path('', ya_profile_view, name='my'),
]
