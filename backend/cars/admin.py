from django.contrib import admin
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _

from django.db.models import Avg

from .models import Car

class PriceRangeFilter(admin.SimpleListFilter):
    title = _('Price Range')
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return [
            ('0-10000', _('0 - 10,000')),
            ('10001-30000', _('10,001 - 30,000')),
            ('30001-50000', _('30,001 - 50,000')),
            ('50001-70000', _('50,001 - 70,000')),
            ('70001-90000', _('70,001 - 90,000')),
            ('90001-110000', _('90,001 - 110,000')),
            ('110001-150000', _('110,001 - 150,000')),
            ('150001-200000', _('150,001 - 200,000')),
            ('250001-300000', _('250,001 - 300,000')),
            # Add more ranges as needed
        ]

    def queryset(self, request, queryset):
        if self.value():
            min_price, max_price = map(float, self.value().split('-'))
            return queryset.filter(price__gte=min_price, price__lte=max_price)
        return queryset

class MileageRangeFilter(admin.SimpleListFilter):
    title = _('Mileage Range')
    parameter_name = 'mileage_range'

    def lookups(self, request, model_admin):
        return [
                ('0-10', _('0 - 10')),
                ('11-30', _('11 - 30')),
                ('31-50', _('31 - 50')),
                ('51-70', _('51 - 70')),
                ('71-90', _('71 - 90')),
                ('91-110', _('91 - 110')),
                ('111-150', _('111 - 150')),
                ('151-200', _('151 - 200')),
                ('201-250', _('201 - 250')),
            # we can add more range if we want
        ]

    def queryset(self, request, queryset):
        if self.value():
            min_price, max_price = map(float, self.value().split('-'))
            return queryset.filter(mileage__gte=min_price, mileage__lte=max_price)
        return queryset

def calculate_average_price(modeladmin, request, queryset, brand):
    # Filter cars for the specified brand
    brand_cars = queryset.filter(brand=brand)

    # Replace null 'price' with 0 for the average calculation
    brand_cars = brand_cars.annotate(price_with_zero=Coalesce('price', 0))

    # Calculate the average price
    average_price = brand_cars.aggregate(Avg('price_with_zero'))['price_with_zero__avg']

    # Display the result to the user
    if average_price is not None:
        message = f'The average price for {brand} cars is: {average_price:.2f}'
    else:
        message = f'No data available for the average price of {brand} cars.'

    modeladmin.message_user(request, message)

calculate_average_price.short_description = 'Calculate Average Price'



class CarAdmin(admin.ModelAdmin):
    list_display = ('car_name', 'brand', 'fuel_type', 'mileage', 'price')
    list_filter = (PriceRangeFilter, MileageRangeFilter, 'fuel_type', 'brand')  #filters in panel on right
    search_fields = ('car_name', 'brand')
    actions = []
    brands = Car.objects.values_list('brand', flat=True).distinct()
    ordering = ['car_name', 'brand', 'fuel_type', 'mileage', 'price']

    for brand in brands:
        def create_action(brand=brand):
            def action_func(modeladmin, request, queryset):
                calculate_average_price(modeladmin, request, queryset, brand)

            action_func.short_description = f'Calculate Average Price for {brand} Cars'
            return action_func

        action = create_action(brand)
        setattr(action, '__name__', f'calculate_average_price_{brand.lower()}')
        actions.append(action)


admin.site.register(Car, CarAdmin)
