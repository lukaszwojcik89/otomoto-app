from django.db import models

class Car(models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year_of_production = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Add other fields as needed

    def __str__(self):
        return f"{self.make} {self.model} ({self.year_of_production})"
