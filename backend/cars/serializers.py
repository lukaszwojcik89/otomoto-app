from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['car_name', 'brand', 'fuel_type', 'mileage', 'price']
