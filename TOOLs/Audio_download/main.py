from youtube_playlist import get_playlist_urls
from audio_srt_download import download_video_srt
from audio_clip import srt_to_audio_clips
import os
import re

def rename_files_to_episode(folder_path, regular_expression):
    for filename in os.listdir(folder_path):
        match = re.search(regular_expression, filename, re.IGNORECASE)
        if match:
            ep_number = match.group()
            new_filename = ep_number + os.path.splitext(filename)[1]  # Keep the original file extension
            original_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            os.rename(original_file_path, new_file_path)
            print(f"Renamed '{filename}' to '{new_filename}'")
    return new_filename[:-4]


def start_downloading(playlist_url, audio_name):
    video_urls = get_playlist_urls(playlist_url)
    path = 'D:/CASPER/Temp/%(title)s.%(ext)s'
    ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg.exe'
    for url in reversed(video_urls):

        print(f"Downloading AUDIO & SRT from {url}")
        download_video_srt(url, path, ffmpeg_path)

        new_filename = rename_files_to_episode('D:/Casper/Temp', r'\bEP\d+\b')

        print(f"Seperating audio clips")
        try:
            srt_to_audio_clips(f"D:/CASPER/Temp/{new_filename}.wav", f"D:/CASPER/Temp/{new_filename}.srt", f"D:/Casper/Taiwanese_youtube/{audio_name}_{new_filename}", f"{audio_name}_{new_filename}")
            print(f"[Finished] '{audio_name}_{new_filename}' is completed.")
        except:
            print(f"[ERROR!!!] '{audio_name}_{new_filename}' is corrupted.")


if __name__ ==  "__main__":
    playlist_url = "https://www.youtube.com/watch?v=RRPBOCqO0wg&list=PL02zpjjwMEjp_X-66jIMYOtgdgK46rNsK&pp=iAQB"
    audio_name = "billionaire_story"
    start_downloading(playlist_url, audio_name)