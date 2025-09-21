from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required(login_url='/login')
def object_list(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(user=request.user)

    context = {
        "npm": "240123456",  # replace with your own ID if required
        "name": request.user.username,
        "class": "PBP A",
        "objects": products,
        "last_login": request.COOKIES.get("last_login", "Never"),
    }
    return render(request, "main/main.html", context)



def add_object(request):
    form = ProductForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)   # don’t save immediately
        product.user = request.user         # link product to the current user
        product.save()
        return redirect("main:object_list")

    context = {
        "form": form
    }
    return render(request, "main/create_product.html", context)

@login_required(login_url='/login')
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

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'main/register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:object_list"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'main/login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response