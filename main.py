import ffmpeg
from pytube import YouTube
from pytube.innertube import _default_clients
import os
import gradio as gr
import time

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

def download_video(yt_link, requirefilp):

    video_require = YouTube(yt_link).streams.filter(progressive=False).order_by('resolution').desc().first().download()
    video_old = os.path.basename(video_require)
    file_root, file_ext = os.path.splitext(video_old)
    video_new = f"{file_root}_mp4merge{file_ext}"
    video_path = os.path.join(os.path.dirname(video_require), video_new)
    os.rename(video_require, video_new)
    
    audio_require = YouTube(yt_link).streams.filter(only_audio=True).order_by('abr').desc().first().download()
    audio_old = os.path.basename(audio_require)
    file_root, file_ext = os.path.splitext(audio_old)
    audio_new = f"{file_root}_mp3merge{file_ext}"
    audio_path = os.path.join(os.path.dirname(audio_require), audio_new)
    os.rename(audio_require, audio_new)
    
    stream = ffmpeg.input(video_new)
    audio = ffmpeg.input(audio_new)
    if('영상 뒤집기' in requirefilp):
        stream = ffmpeg.hflip(stream)
    stream = ffmpeg.output(stream, audio, video_require)
    ffmpeg.run(stream)
    yield video_require
    time.sleep(3)
    os.remove(video_new)
    os.remove(audio_new)
    os.remove(video_require)

def download_audio(yt_link):
    audio_require = YouTube(yt_link).streams.filter(only_audio=True).order_by('abr').desc().first().download()
    audio_old = os.path.basename(audio_require)
    file_root,file_ext = os.path.splitext(audio_old)
    audio_want = f"{file_root}.mp3"
    ffmpeg.input(audio_old).output(audio_want, format="mp3", acodec='mp3').run()
    yield audio_want
    time.sleep(3)
    os.remove(audio_old)
    os.remove(audio_want)

with gr.Blocks() as app: 
    with gr.Tab("MP4 다운받기"):
        with gr.Column():
            mp4_inputs=gr.Text(label="유튜브 링크")
            mp4_inputs_checkbox=gr.CheckboxGroup(["영상 뒤집기"], label="옵션")
            mp4_outputs=gr.Video(label="다운로드 영상")
            mp4_button1 = gr.Button("변환")
            mp4_button1.click(download_video, inputs=[mp4_inputs, mp4_inputs_checkbox], outputs=[mp4_outputs])
    with gr.Tab("MP3 다운받기"):
        with gr.Column():
            mp3_inputs=gr.Text(label="유튜브 링크")
            mp3_outputs=gr.Audio(label="다운로드 음원")
            mp3_button2 = gr.Button("변환")
            mp3_button2.click(download_audio, inputs=[mp3_inputs], outputs=[mp3_outputs])

app.launch()