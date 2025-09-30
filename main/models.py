from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    # Fixed categories + an 'other' bucket
    CATEGORY_SHOES = "shoes"
    CATEGORY_APPAREL = "apparel"
    CATEGORY_HARDWARE = "hardware"
    CATEGORY_STORES = "stores"
    CATEGORY_ACCESSORIES = "accessories"
    CATEGORY_BALLS = "balls"
    CATEGORY_OTHER = "other"

    CATEGORY_CHOICES = [
        (CATEGORY_SHOES, "Shoes"),
        (CATEGORY_APPAREL, "Apparel"),
        (CATEGORY_HARDWARE, "Hardware"),
        (CATEGORY_STORES, "Stores"),
        (CATEGORY_ACCESSORIES, "Accessories"),
        (CATEGORY_BALLS, "Balls"),
        (CATEGORY_OTHER, "Other"),
    ]

    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    category_other = models.CharField(max_length=50, blank=True, null=True)

    is_featured = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    brand = models.CharField(max_length=100, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def category_label(self):
        if self.category == self.CATEGORY_OTHER and self.category_other:
            return self.category_other
        return self.get_category_display()

    def __str__(self):
        return self.name
