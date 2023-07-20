from django.db import models

# Create your models here.


class Device(models.Model):
    device_name = models.CharField(max_length=255, null=True, blank=True)


class DeviceStatus(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=10, decimal_places=8)
    long = models.DecimalField(max_digits=10, decimal_places=8)
    timestamp = models.DateTimeField(null=True, blank=True)
    sts = models.DateTimeField(null=True, blank=True)
    speed = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

