from django.urls import path,include
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("imageupload/", views.add_image, name="imageupload"),
    path("delete/<str:uuid>", views.deleteImage, name="delete"),
    path("showingMap/", views.showMap, name="showmap"),
    path("search/", views.searchData, name="search")
]
