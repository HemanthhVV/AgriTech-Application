from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from .utils import ProcessImage
from .models import UploadedData
from django.contrib import messages

processor = ProcessImage()

def deleteImage(request,uuid:str):
    if request.method == 'POST':
        getData = UploadedData.objects.get(user=request.user,uuid=uuid)
        path_of_media = os.path.join(settings.BASE_DIR,'media',str(getData.image))
        os.remove(path_of_media)
        getData.delete()
        messages.error(request,message=f"File ID {uuid} deleted sucesssfully")
        return redirect('home')

def showMap(request):
    coodinates = UploadedData.objects.all()
    context = {
        'images':coodinates
    }
    # import pdb
    # pdb.set_trace()
    return render(request,'imageUploader/map.html',context=context)


@login_required(login_url='/authentication/login')
def index(request):
    images = UploadedData.objects.all()

    if not images:
        return render(request=request,template_name='imageUploader/empty.html')

    context = {
        "images":images,
    }
    # import pdb
    # pdb.set_trace()
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

        latitude = coordinates[0].replace(' ','').split(':')[1]
        longitude = coordinates[1].replace(' ','').split(':')[1]
        timeOfPhoto,farmerID,farmerName = processor.makePreciseText(coordinates[2:])

        UploadedData.objects.create(
            image = image,
            latitude = latitude,
            longitude = longitude,
            timeOfPhoto = timeOfPhoto,
            farmerID = farmerID,
            farmerName = farmerName,
            user= request.user
        )
        print('Completed Processing')
        print('Saved')

        os.remove(temp_path)
        messages.success(request,"File added sucessfully")
        return redirect('home')  # Redirect after saving
    return render(request, 'imageUploader/uploader.html')
