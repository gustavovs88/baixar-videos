import requests
import os
from django.shortcuts import render
from .forms import VideoUrlForm
from django.contrib import messages
import pafy
from django.http import StreamingHttpResponse, FileResponse, response
from django.core.files import File

import re


def index(request):
    if request.method == 'POST':
        form = VideoUrlForm(request.POST)
        video_url = form['video_url'].value()
        with open('/etc/api_key') as f:
            api_key = f.read().strip()
        if form.is_valid():
            pafy.set_api_key(api_key)
            yt_object = pafy.new(video_url)
            video_title = yt_object.title
            video_length = yt_object.duration
            video_thumb = yt_object.bigthumbhd
            video_author = yt_object.author
            video_views = yt_object.viewcount
            video_publication_year = list(yt_object.published)
            video_publication_year = ''.join(video_publication_year[0:4])
            video_streams = yt_object.streams
            best_stream = yt_object.getbest()
            best_stream = {
                'url': best_stream.url,
                'resolucao': best_stream.resolution,
                'extensao': best_stream.extension,
                'tamanho': round(best_stream.get_filesize()/1048576, 1),
            }
            stream_object = {}
            for stream in video_streams:
                stream_object[stream] = {
                    'url': stream.url,
                    'resolucao': stream.resolution,
                    'extensao': stream.extension,
                    'tamanho': round(stream.get_filesize()/1048576, 1),
                }
            audio_streams = yt_object.audiostreams
            audio_object = {}
            for audio_stream in audio_streams:
                audio_object[audio_stream] = {
                    'url': audio_stream.url,
                    'qualidade': audio_stream.quality,
                    'extensao': audio_stream.extension,
                    'tamanho': round(audio_stream.get_filesize() / 1048576, 1),
                }
            video_only_streams = yt_object.videostreams
            video_only_object = {}
            for video_only_stream in video_only_streams:
                video_only_object[video_only_stream] = {
                    'url': video_only_stream.url,
                    'resolucao': video_only_stream.resolution,
                    'extensao': video_only_stream.extension,
                    'tamanho': round(video_only_stream.get_filesize() / 1048576, 1),
                }
            context = {
                'titulo': video_title,
                'duracao': video_length,
                'imagem': video_thumb,
                'form': form,
                'video_objeto': stream_object,
                'audio_objeto': audio_object,
                'so_video_objeto': video_only_object,
                'autor': video_author,
                'visualizacoes': video_views,
                'ano_publicacao': video_publication_year,
                'melhor_video': best_stream,
            }


            # r = requests.get(context['video_objeto'], stream=True)
            # video_data = r.content
            # video_mime_type = r.headers['Content-Type']

            # add_context = {'video_mime_type': video_mime_type, 'video_data': video_data}
            # context.update(add_context)

            # def gen():
            # with open(context['titulo'], 'wb') as fd:
            #    for chunk in r.iter_content(chunk_size=128):
            #        yield chunk
            # response = StreamingHttpResponse(streaming_content=gen(), headers={
            #    'Content-Type': 'video/mp4',
            #    'Content-Disposition': 'attachment; filename="mydownload"',
            # })

            # file_attach = FileResponse(open(context['titulo'], 'rb'), as_attachment=True)
            # print(r.status_code)
            # yt.streams.get_lowest_resolution().download()
            # print(context)
            return render(request, 'index.html', context)

    else:
        messages.error(request, 'Erro ao fazer o Download')
        form = VideoUrlForm()
        context = {
            'titulo': False,
            'duracao': False,
            'autor': False,
            'streamquery': False,
            'form': form,
            'video_url': False

        }
        return render(request, 'index.html', context)


def video_download(request):
    if request.method == "POST":
        video_url = request.POST.get('video_url')
        titulo = re.sub('[^A-Za-z0-9\s]+', '', request.POST.get('titulo'))
        extensao = request.POST.get('extensao')

        r = requests.get(video_url, stream=True)
        def gen():
            for chunk in r.iter_content(chunk_size=128):
                yield chunk
        response = StreamingHttpResponse(streaming_content=gen(), headers={
                'Content-Type': f'video/{extensao}',
                'Content-Disposition': f'attachment; filename={titulo}.{extensao}',
            })
        return response
    else:
        return render(request, 'index.html')
