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
    uploaded_time = models.DateTimeField(auto_now_add=True)
    details = models.TextField()
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='uploaded_images')

    def __str__(self):
        return f'Image - {self.uuid} created by {self.user} at {self.uploaded_time}'
