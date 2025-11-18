from django.urls import path
from .views import (
    object_list, add_object, detail_object,
    show_xml, show_json, 
    show_xml_by_id, show_json_by_id,
    register, edit_object, delete_object, ajax_delete_product,
    ajax_create_product, ajax_update_product, ajax_login,
    ajax_register, get_product_form, get_edit_product_form,
    ajax_product_list, proxy_image, create_product_flutter,
)
from main.views import login_user, logout_user

app_name = "main"

urlpatterns = [
    path("", object_list, name="object_list"),
    path("add/", add_object, name="add_object"),
    path("detail/<int:obj_id>/", detail_object, name="detail_object"),

    # New API endpoints
    path("xml/", show_xml, name="show_xml"),
    path("json/", show_json, name="show_json"),
    path("xml/<int:obj_id>/", show_xml_by_id, name="show_xml_by_id"),
    path("json/<int:obj_id>/", show_json_by_id, name="show_json_by_id"),
    
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    
    path("product/<int:id>/edit/", edit_object, name="edit_object"),
    path('product/<int:id>/delete/', delete_object, name='delete_object'),
    
    path('ajax/delete_product/<int:pk>/', ajax_delete_product, name='ajax_delete_product'),
    path('ajax/create_product/', ajax_create_product, name='ajax_create_product'),
    path('ajax/update_product/<int:pk>/', ajax_update_product, name='ajax_update_product'),
    
    path('ajax/login/', ajax_login, name='ajax_login'),
    path('ajax/register/', ajax_register, name='ajax_register'),
    
    path('ajax/get_product_form/', get_product_form, name='get_product_form'),
    path('ajax/get_edit_form/<int:pk>/', get_edit_product_form, name='get_edit_product_form'),
    
    path('ajax/product_list/', ajax_product_list, name='ajax_product_list'),
    
    path('proxy-image/', proxy_image, name='proxy_image'),
    path('create-product-flutter/', create_product_flutter, name='create_product_flutter'),

]
