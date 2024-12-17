from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import os
from .utils import ProcessImage
from .models import UploadedData

processor = ProcessImage()

@login_required(login_url='/authentication/login')
def index(request):
    images = UploadedData.objects.all()
    details = UploadedData.objects.values_list('details')

    context = {
        "images":images,
        "details":details
    }
    return render(request,'imageUploader/index.html',context=context)

def add_image(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']

        # image_name = image.name
        # image = processor.preprocessimage(image)
        # temp_path = os.path.join('temp',image_name)

        temp_path = os.path.join('temp',image.name)
        with open(temp_path,'wb+') as temp_file:
            for chunk in image.chunks():
                temp_file.write(chunk)

        print('Image Recevied Sucessfull')
        print('Started Processing')
        try:
            listValues = processor.processingImage(temp_path,image.name)
        except:
            return "Unable to parse the image"

        if len(listValues) > 2:
            coordinates = processor.getCoordinates(listValues)
        else:
            return "Unable to parse the image"

        import pdb
        pdb.set_trace()

        latitude = coordinates[0]
        longitude = coordinates[1]
        details = '?'.join(listValues[2:])

        UploadedData.objects.create(
            image = image,
            latitude = latitude,
            longitude = longitude,
            details = details,
            user= request.user
        )
        print('Completed Processing')
        print('Saved')

        os.remove(temp_path)

        return redirect('home')  # Redirect after saving
    return render(request, 'imageUploader/uploader.html')
