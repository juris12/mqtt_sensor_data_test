from . import views
from django.urls import path

urlpatterns = [
    path('', views.building_list, name='building_list'),
    path('sensor_data_list/<str:id>', views.sensor_data_list, name='sensor_data_list'),
    path('suggestions/', views.building_names),
    path('sensor/detail/<int:id>/', views.sensor_detail, name='sensor_detail'),
    path('sensor/<int:sensor_id>/field/<int:field_id>/', views.sensor_field_detail, name='sensor_field_detail'),
]