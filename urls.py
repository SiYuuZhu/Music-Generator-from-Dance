from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'web'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='web/index.html'), name='index'),
    path('video/upload/', views.UploadVideoView.as_view(), name='video_upload'),
    path('record/', TemplateView.as_view(template_name='web/record.html'), name='record'),
    path('generate/<int:id>/', views.GenerateView.as_view(), name='generate'),
    path('wait/<int:id>/', views.WaitView.as_view(), name='wait'),
    path('result/<int:id>/', views.ResultView.as_view(), name='result'),
    path('download/<str:target>/<int:id>/', views.DownloadView.as_view(), name='download'),
    path('intro/', TemplateView.as_view(template_name='web/intro.html'), name='intro'),  # above are for user
    path('generate/list/', views.ListGenerateView.as_view(), name='generate_list'),  # above are for manager
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
