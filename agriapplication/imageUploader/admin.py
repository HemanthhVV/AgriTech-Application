from django.contrib import admin
from .models import UploadedData

class ToShowAttributesInExpenses(admin.ModelAdmin):
    list_display = (
        'ids',
        'uuid',
        'image',
        'latitude',
        'longitude',
        'uploaded_time',
        'farmerID',
        'farmerName',
        'timeOfPhoto',
    )

admin.site.register(UploadedData,ToShowAttributesInExpenses)

