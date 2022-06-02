from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', UploadFileView.as_view(), name='upload-file'),
    path('viewdata/', FileDataAPIView.as_view(), name='view-file-data'),
    path('filedata/', views.FileViewData),
    path('signin/', RegisterAPI.as_view(), name='register-user'),
]
