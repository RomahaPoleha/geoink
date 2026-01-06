from django.db import models
from django.contrib.auth.models import User

class GeoPin(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class PinMemo(models.Model):
    pin = models.ForeignKey(GeoPin, on_delete=models.CASCADE, related_name="memos")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
