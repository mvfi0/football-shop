from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # include all the fields you want to edit via the form
        fields = [
            "name", "price", "description", "thumbnail",
            "category", "is_featured", "stock", "rating", "brand",
        ]
        # (optional) nicer widgets
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "thumbnail": forms.URLInput(attrs={"placeholder": "https://..."}),
            "is_featured": forms.CheckboxInput(),
        }
        labels = {
            "is_featured": "Featured product?",
        }
