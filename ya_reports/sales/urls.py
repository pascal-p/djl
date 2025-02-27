from django.urls import path
from .views import (
    home_view,
    SaleListView,
    SaleDetailView,
)
app_name = 'sales'

urlpatterns = [
    path('', home_view, name='home'), # the main view hence ''

    path('sales/', SaleListView.as_view(), name='list'),
    path('sales/<pk>/', SaleDetailView.as_view(), name='detail'),
]
