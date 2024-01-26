from __future__ import unicode_literals
import yt_dlp
import os

ydl_opts = {
    'format': 'bestaudio/best',
    'ffmpeg_location': os.path.realpath('C:/ffmpeg/bin/ffmpeg.exe'),
    'outtmpl': 'D:/Casper/Weight/output.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    url = "https://www.youtube.com/watch?v=exxF_ZvHw5U"
    ydl.download([url])
