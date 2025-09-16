from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product
from django.http import HttpResponse
from django.core import serializers

def object_list(request):
    products = Product.objects.all()
    return render(request, "main/main.html", {"objects": products})

def add_object(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("main:object_list")
    return render(request, "main/create_product.html", {"form": form})

def detail_object(request, obj_id):
    product = get_object_or_404(Product, id=obj_id)
    return render(request, "main/product_detail.html", {"product": product})


# Show all products in XML
def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(
        serializers.serialize("xml", data),
        content_type="application/xml"
    )

# Show all products in JSON
def show_json(request):
    data = Product.objects.all()
    return HttpResponse(
        serializers.serialize("json", data),
        content_type="application/json"
    )

# Show one product in XML (by id)
def show_xml_by_id(request, obj_id):
    data = Product.objects.filter(pk=obj_id)
    return HttpResponse(
        serializers.serialize("xml", data),
        content_type="application/xml"
    )

# Show one product in JSON (by id)
def show_json_by_id(request, obj_id):
    data = Product.objects.filter(pk=obj_id)
    return HttpResponse(
        serializers.serialize("json", data),
        content_type="application/json"
    )
