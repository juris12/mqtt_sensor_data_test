from . import views
from django.urls import path

urlpatterns = [
    path('', views.building_list, name='building_list'),
    path('sensor_data_list/<str:id>', views.sensor_data_list, name='sensor_data_list'),
    path('suggestions/', views.building_names),
]