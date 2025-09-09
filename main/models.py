from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)  # Item name
    price = models.IntegerField()  # Item price
    description = models.TextField()  # Item description
    thumbnail = models.URLField()  # Item image
    category = models.CharField(max_length=100)  # Item category
    is_featured = models.BooleanField(default=False)  # Featured status
    
    # Optional attributes (you can remove or modify these if not needed)
    stock = models.IntegerField(default=0)  # Stock count
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)  # Rating (e.g., 4.5)
    brand = models.CharField(max_length=100, null=True, blank=True)  # Brand name

    def __str__(self):
        return f"{self.name} - {self.category}"
