from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string

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

def ajax_product_list(request):
    """
    Return an HTML fragment containing the product grid (no layout).
    Uses same filtering logic as object_list (so it respects ?filter= and ?category=).
    """
    qs = Product.objects.all()

    # --- All / My products filter (same as object_list) ---
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'my' and request.user.is_authenticated:
        qs = qs.filter(user=request.user)

    # --- Category filter (same as object_list) ---
    category_param = (request.GET.get('category') or '').strip()
    if category_param:
        values = {v for v, _ in Product.CATEGORY_CHOICES}
        labels_to_values = {lbl.lower(): val for val, lbl in Product.CATEGORY_CHOICES}
        candidate = category_param.lower()
        if candidate in values:
            qs = qs.filter(category=candidate)
        elif candidate in labels_to_values:
            qs = qs.filter(category=labels_to_values[candidate])

    context = {
        'object_list': qs,
        'user': request.user,
    }

    html = render_to_string('main/_product_list_fragment.html', context, request=request)
    return HttpResponse(html)

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
    
    if sort_by == 'price_asc':
        data = data.order_by('price')
    elif sort_by == 'price_desc':
        data = data.order_by('-price')
        
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
    messages.info(request, "You have been logged out successfully.")

    # This redirect is the key. It must point to a page
    # with the message-displaying script.
    response = HttpResponseRedirect(reverse('main:object_list'))
    
    response.delete_cookie('last_login')
    return response

def edit_object(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("main:object_list")

    context = {
        "form": form,
        "object": product
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

def ajax_delete_product(request, pk):
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return JsonResponse({'status': 'success', 'message': 'Product deleted successfully.'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def ajax_create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            
            # ADD THIS LINE for the toast notification
            messages.success(request, "Product created successfully!")
            
            redirect_url = reverse('main:object_list')
            return JsonResponse({'status': 'success', 'redirect_url': redirect_url})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def ajax_update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            # ADD THIS LINE for the toast notification
            messages.success(request, "Product updated successfully!")
            
            redirect_url = reverse('main:object_list')
            return JsonResponse({'status': 'success', 'redirect_url': redirect_url})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def ajax_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            
            redirect_url = reverse('main:object_list')

            # 1. Create the JSON response object
            response = JsonResponse({'status': 'success', 'redirect_url': redirect_url})
            
            # 2. Set the cookie on the response
            response.set_cookie('last_login', str(datetime.datetime.now()))
            
            # 3. Return the response with the cookie
            return response
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid username or password.'
            }, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def ajax_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account registered successfully!")
            
            # CHANGE THIS LINE to redirect to the main page
            redirect_url = reverse('main:object_list') 
            
            return JsonResponse({'status': 'success', 'redirect_url': redirect_url})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        
def get_product_form(request):
    form = ProductForm()
    return render(request, 'main/_product_form.html', {'form': form, 'action_url': reverse('main:ajax_create_product')})

@login_required(login_url='/login/')
def get_edit_product_form(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(instance=product)
    
    # We pass the form_id and the correct update URL to the template
    context = {
        'form': form,
        'form_id': 'update-product-form',
        'action_url': reverse('main:ajax_update_product', kwargs={'pk': pk})
    }
    return render(request, 'main/_product_form.html', context)