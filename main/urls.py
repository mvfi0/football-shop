from django.urls import path
from django.urls import path
from .views import (
    object_list, 
    add_object, 
    detail_object,
    show_xml, 
    show_json, 
    show_xml_by_id, 
    show_json_by_id
)

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
]
