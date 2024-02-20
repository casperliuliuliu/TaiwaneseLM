from youtube_playlist import get_playlist_urls
from audio_srt_download import download_video_srt
from audio_clip import srt_to_audio_clips

def start_downloading(playlist_url, audio_name):
    video_urls = get_playlist_urls(playlist_url)
    path = 'D:/CASPER/Temp/output.%(ext)s'
    ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg.exe'
    video_index = 1
    for url in reversed(video_urls):

        print(f"Downloading AUDIO & SRT from {url}")
        download_video_srt(url, path, ffmpeg_path)

        print(f"Seperating audio clips")
        clips_transcriptions = srt_to_audio_clips("D:/CASPER/Temp/output.wav", "D:/CASPER/Temp/output.zh-TW.srt", f"D:/Casper/Taiwanese_youtube/{audio_name}_{video_index}", f"{audio_name}_{video_index}")
        video_index +=1
        print("[Finished]")

if __name__ ==  "__main__":
    playlist_url = "https://www.youtube.com/watch?v=RRPBOCqO0wg&list=PL02zpjjwMEjp_X-66jIMYOtgdgK46rNsK&pp=iAQB"
    audio_name = "billionaire_story"
    start_downloading(playlist_url, audio_name)