# cars/views.py
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Car
from .serializers import CarSerializer

class CarListView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    pagination_class = PageNumberPagination
