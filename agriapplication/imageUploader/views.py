from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os,json
from .utils import ProcessImage
from .models import UploadedData
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
import pdb

processor = ProcessImage()

@login_required(login_url='/authentication/login')
def searchData(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get("searchField")
        parsedData = (
            UploadedData.objects.filter(farmerID__istartswith=search_str,user = request.user) |
            UploadedData.objects.filter(farmerName__icontains=search_str,user = request.user)
        )
        search_data = parsedData.values()
        return JsonResponse(list(search_data),safe=False)

@login_required(login_url='/authentication/login')
def deleteImage(request,uuid:str):
    if request.method == 'POST':
        getData = UploadedData.objects.get(user=request.user,uuid=uuid)
        path_of_media = os.path.join(settings.BASE_DIR,'media',str(getData.image))
        os.remove(path_of_media)
        getData.delete()
        messages.error(request,message=f"File ID {uuid} deleted sucesssfully")
        return redirect('home')

@login_required(login_url='/authentication/login')
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
    images = UploadedData.objects.filter(user=request.user)

    if not images:
        return render(request=request,template_name='imageUploader/empty.html')

    context = {
        "images":images,
    }
    # import pdb
    # pdb.set_trace()
    return render(request,'imageUploader/index.html',context=context)

@login_required(login_url='/authentication/login')
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
            os.remove(temp_path)
            messages.error(request,"Unable to parse the image.")
            return redirect('home')

        if len(listValues) > 2:
            coordinates = processor.getCoordinates(listValues)
        else:
            os.remove(temp_path)
            messages.info(request,"Unable to get the co-ordinates, Check the image has co-ordinates")
            return redirect('home')

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
