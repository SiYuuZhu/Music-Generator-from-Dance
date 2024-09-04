from django.views import View, generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import FileResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.core.files.base import File

import threading

from .models import Dance, Music, DanceFeature, MusicSeed
from .main import main


# Create your views here.
class UploadVideoView(View):
    template_name = 'web/check.html'

    def post(self, request):
        file = request.FILES.get('file')
        dance = Dance.objects.create(file=file)
        return render(request, self.template_name, {'dance': dance})


class GenerateView(View):
    template_name = 'web/wait.html'

    def get(self, request, **kwargs):
        id = self.kwargs.get('id')
        dance = Dance.objects.get(id=id)
        music = Music.objects.create(dance=dance)
        dance_path = dance.file.url

        thread = threading.Thread(target=generate, args=(dance_path, music,))  # 後面繼續跑，先回傳response
        thread.start()
        return render(request, self.template_name, {'music_id': music.id})


class WaitView(View):
    template_name = 'web/wait.html'

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        music = Music.objects.get(id=id)

        if music.completed:  # 前端不斷刷新請求，檢查是否生成完成
            return redirect('/result/' + str(id) + '/')
        else:
            return render(request, self.template_name, {'music_id': id})


class ResultView(View):
    template_name = 'web/result.html'

    def get(self, request, **kwargs):
        id = self.kwargs.get('id')
        music = Music.objects.get(id=id)

        return render(request, self.template_name, {'music': music, 'dance': music.dance})


class DownloadView(View):
    template_name = 'web/result.html'

    def get(self, request, **kwargs):
        target = self.kwargs.get('target')  # music or dance
        id = self.kwargs.get('id')
        print('target:', target)

        if target == 'music':
            music = get_object_or_404(Music, id=id)
            filename = music.file.name
            file = open(music.file.path, 'rb')
        elif target == 'dance':
            dance = get_object_or_404(Dance, id=id)
            filename = dance.file.name
            file = open(dance.file.path, 'rb')
        elif target == 'combine':
            music = get_object_or_404(Music, id=id)
            filename = music.combine.name
            file = open(music.combine.path, 'rb')

        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="' + filename + '"'
        return response


class ListGenerateView(generic.ListView):
    template_name = 'web/generate_list.html'
    model = Dance
    context_object_name = 'generate_list'


def generate(dance_path, music):
    music_filepath, video_filepath = main.generate(dance_path, music.id)
    file = File(open(music_filepath, 'rb'))
    print('break point 1')
    music.file = file
    combine = File(open(video_filepath, 'rb'))
    print('break point 2')
    music.combine = combine
    music.completed = True
    music.save()
    print('break point 3')
