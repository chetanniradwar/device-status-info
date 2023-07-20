from django.urls import path

from .views import load_data_csv_to_db, get_device_latest_info, get_device_start_and_end_location, \
    get_all_location_points

urlpatterns = [
    path('load_data_csv_to_db/', load_data_csv_to_db),
    path('get_device_latest_info/', get_device_latest_info),
    path('get_device_start_and_end_location/', get_device_start_and_end_location),
    path('get_all_location_points/', get_all_location_points),
    ]
