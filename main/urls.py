from django.urls import path
from .views import (
    object_list, 
    add_object, 
    detail_object,
    show_xml, 
    show_json, 
    show_xml_by_id, 
    show_json_by_id,
    register,
    edit_object,
    delete_object,
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
]
