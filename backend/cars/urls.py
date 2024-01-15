from django.urls import path
from .views import CarListView

urlpatterns = [
    path('cars/', CarListView.as_view(), name='car-list'),
    # Add other views and URL patterns as needed
]
