from django.urls import path
from django.conf.urls import url
from .views import index, video_download

urlpatterns = [
    path('', index, name='index'),
    path('video_download', video_download, name='video_download')
]
