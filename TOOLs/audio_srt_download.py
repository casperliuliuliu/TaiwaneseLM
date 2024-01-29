from __future__ import unicode_literals
import yt_dlp
import os

def download_video_srt(url, path, ffmpeg_path):
    ydl_opts = {
    'format': 'bestaudio/best',
    'ffmpeg_location': os.path.realpath(ffmpeg_path),
    'outtmpl': path,
    'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        },
        {
            'key': 'FFmpegSubtitlesConvertor',
            'format': 'srt',
        },
        ],
        'writesubtitles': True,
    }

    yt_dlp.YoutubeDL(ydl_opts).download([url])

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=FPYl7nIKRbA"
    path = '/Users/liushiwen/Desktop/WINTERVACATION/output1.%(ext)s'
    path = 'D:/CASPER/output1.%(ext)s'
    ffmpeg_path = '/Users/liushiwen/Desktop/WINTERVACATION/ffmpeg'
    ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg.exe'
    download_video_srt(url, path, ffmpeg_path)