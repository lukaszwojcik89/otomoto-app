import django_filters
from .models import Car



class CarFilter(django_filters.FilterSet):
    class Meta:
        model = Car
        fields = ['fuel_type', 'brand']
