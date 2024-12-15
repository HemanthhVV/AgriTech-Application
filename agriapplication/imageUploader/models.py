from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class UploadedData(models.Model):
    ids = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    image = models.ImageField(upload_to='uploaded_images/')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.TimeField()
    uploaded_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='uploaded_images')