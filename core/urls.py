from django.urls import path
from django.conf.urls import handler500, url
from .views import index, video_download, error_500

urlpatterns = [
    path('', index, name='index'),
    path('video_download', video_download, name='video_download'),
    
]
handler500 = 'core.views.error_500'