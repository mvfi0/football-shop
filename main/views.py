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
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.views.decorators.http import require_POST

@login_required(login_url='/login')
def object_list(request):
    qs = Product.objects.all()

    # --- All / My products filter ------------------------------------------
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'my' and request.user.is_authenticated:
        qs = qs.filter(user=request.user)

    # --- Category filter -----------------------------------------------------
    # Accept either the stored value (e.g. 'shoes') or a label (e.g. 'Shoes').
    category_param = (request.GET.get('category') or '').strip()
    if category_param:
        values = {v for v, _ in Product.CATEGORY_CHOICES}                      # {'shoes','apparel',...}
        labels_to_values = {lbl.lower(): val for val, lbl in Product.CATEGORY_CHOICES}

        candidate = category_param.lower()
        if candidate in values:
            qs = qs.filter(category=candidate)
        elif candidate in labels_to_values:
            qs = qs.filter(category=labels_to_values[candidate])
        # else: unknown category → leave qs as-is

    context = {
        'object_list': qs,
        'last_login': request.COOKIES.get('last_login', ''),
        'active_filter': filter_type,
        'active_category': (request.GET.get('category') or '').lower(),
        'CATEGORY_CHOICES': Product.CATEGORY_CHOICES,   # used by template to render chips
    }
    return render(request, 'main/main.html', context)

@login_required(login_url='/login/')
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

def edit_object(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("main:object_list")

    context = {
        "form": form
    }
    return render(request, "main/edit_product.html", context)

@login_required(login_url="/login")
@require_POST
def delete_object(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this product.")
    product.delete()
    return redirect("main:object_list")