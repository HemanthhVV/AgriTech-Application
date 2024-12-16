from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import os
from .utils import ProcessImage

processor = ProcessImage()

@login_required(login_url='/authentication/login')
def index(request):
    return render(request,'imageUploader/index.html')

def add_image(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        temp_path = os.path.join('temp',image.name)

        with open(temp_path,'wb+') as temp_file:
            for chunk in image.chunks():
                temp_file.write(chunk)

        print('Image Recevied Sucessfull')
        print('Started Processing')
        listValues = processor.processingImage(temp_path)
        print('Completed Processing')
        import pdb
        pdb.set_trace()

        return redirect('home')  # Redirect after saving
    return render(request, 'imageUploader/uploader.html')
