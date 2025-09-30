from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "description",
            "thumbnail",
            "category",
            "category_other",
            "is_featured",
            "stock",
            "rating",
            "brand",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border border-purple-400 rounded-md focus:ring-2 focus:ring-purple-500 focus:outline-none",
                "placeholder": "Enter product name",
            }),
            "price": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border border-purple-400 rounded-md focus:ring-2 focus:ring-purple-500 focus:outline-none",
                "placeholder": "Enter price",
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full px-4 py-2 border border-purple-400 rounded-md focus:ring-2 focus:ring-purple-500 focus:outline-none",
                "placeholder": "Write a description...",
                "rows": 4,
            }),
            "thumbnail": forms.URLInput(attrs={
                "class": "w-full px-4 py-2 border border-purple-400 rounded-md focus:ring-2 focus:ring-purple-500 focus:outline-none",
                "placeholder": "Image URL",
            }),
            "category": forms.Select(attrs={
                "class": "w-full px-4 py-2 border border-purple-400 rounded-md focus:ring-2 focus:ring-purple-500 focus:outline-none",
            }),
            "category_other": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border border-purple-400 rounded-md focus:ring-2 focus:ring-purple-500 focus:outline-none",
                "placeholder": "Other category (if applicable)",
            }),
            "is_featured": forms.CheckboxInput(attrs={
                "class": "h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded",
            }),
            "stock": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border border-purple-400 rounded-md focus:ring-2 focus:ring-purple-500 focus:outline-none",
                "placeholder": "Available stock",
            }),
            "rating": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border border-purple-400 rounded-md focus:ring-2 focus:ring-purple-500 focus:outline-none",
                "placeholder": "Rating (e.g. 4.5)",
                "step": "0.1",
            }),
            "brand": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border border-purple-400 rounded-md focus:ring-2 focus:ring-purple-500 focus:outline-none",
                "placeholder": "Brand name",
            }),
        }
