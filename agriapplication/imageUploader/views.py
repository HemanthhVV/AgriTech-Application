from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url='/authentication/login')
def index(request):
    return render(request,'imageUploader/index.html')

def add_image(request):
    return render(request,'imageUploader/uploader.html')
