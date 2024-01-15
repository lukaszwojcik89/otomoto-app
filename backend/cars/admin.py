from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['car_name', 'brand', 'fuel_type', 'mileage']
    list_filter = ['fuel_type', 'brand']