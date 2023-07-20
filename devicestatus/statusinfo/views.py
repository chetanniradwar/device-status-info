import os
import csv
from datetime import datetime

from .enums import DEFAULT_CACHE_TIMEOUT
from .models import Device, DeviceStatus
from django.core.cache import cache
from django.http import JsonResponse


def load_data_csv_to_db(request):
    try:
        csv_fil_path = os.path.join(os.path.dirname(__file__), 'static/raw_devices_status.csv')

        with open(csv_fil_path) as file:
            reader = csv.reader(file)
            next(reader)  # Advance past the header

            Device.objects.all().delete()
            DeviceStatus.objects.all().delete()

            status_objs_to_create = list()
            for row in reader:
                # print(row)

                device, _ = Device.objects.get_or_create(id=row[0])

                status_objs_to_create.append(DeviceStatus(device=device, lat=row[1], long=row[2], timestamp=row[3],
                                                          sts=row[4], speed=row[5]))

            DeviceStatus.objects.bulk_create(status_objs_to_create, batch_size=1000)
    except Exception as e:
        return JsonResponse({"status": False, "error": str(e)}, status=400)

    return JsonResponse({"status": True}, status=200, safe=False)


def get_device_latest_info(request):
    device_id = request.GET.get("device_id")
    try:
        device_id = int(device_id)
    except Exception as e:
        return JsonResponse({"status": False}, status=400)

    if cache.get(f"dli_{device_id}"):
        return JsonResponse(cache.get(f"dli_{device_id}"), status=200)

    latest_device_status_values = DeviceStatus.objects.filter(device_id=device_id).order_by('-sts').values().first()
    cache.set(f"dli_{latest_device_status_values['device_id']}", latest_device_status_values, DEFAULT_CACHE_TIMEOUT)

    return JsonResponse(latest_device_status_values, status=200)


def get_device_start_and_end_location(request):
    device_id = request.GET.get("device_id")
    try:
        device_id = int(device_id)
    except Exception as e:
        return JsonResponse({"status": False}, status=400)

    if cache.get(f"dsel_{device_id}"):
        return JsonResponse(cache.get(f"dsel_{device_id}"), status=200)

    device_status_qs = DeviceStatus.objects.filter(device_id=device_id).order_by('sts').only('id', 'lat', 'long')

    start_loc_obj = device_status_qs.first()
    end_loc_obj = device_status_qs.last()

    loc_data = {
        "device_id": device_id,
        "start_loc": (start_loc_obj.lat, start_loc_obj.long),
        "end_loc": (end_loc_obj.lat, end_loc_obj.long)
    }

    cache.set(f"dsel_{device_id}", loc_data, DEFAULT_CACHE_TIMEOUT)

    return JsonResponse(loc_data, status=200)


def get_all_location_points(request):
    device_id = request.GET.get("device_id")
    start_time = request.GET.get("start_time")
    end_time = request.GET.get("end_time")

    try:
        device_id = int(device_id)
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return JsonResponse({"status": False, "error": str(e)}, status=400)

    device_status_qs = DeviceStatus.objects.filter(device_id=device_id,
                                                   timestamp__gt=start_time, timestamp__lt=end_time).order_by('-sts')

    loc_points_list = list()
    for device_status_obj in device_status_qs:
        loc_points_list.append((device_status_obj.lat, device_status_obj.long, device_status_obj.timestamp))

    return JsonResponse(loc_points_list, status=200, safe=False)
