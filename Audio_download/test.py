import yt_dlp
import os
import re

def rename_postprocessor(info):
    # Extract episode number from the title
    print(info)
    return
    match = re.search(r'\bEP\d+\b', info, re.IGNORECASE)
    if match:
        ep_number = match.group()
        new_filename = ep_number + '.wav'
        new_filepath = os.path.join(info['filepath'].rsplit(os.path.sep, 1)[0], new_filename)
        os.rename(info['filepath'], new_filepath)
        info['filepath'] = new_filepath
    return [], info

def download_video_srt(url, path, ffmpeg_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': os.path.realpath(ffmpeg_path),
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        },
        {
            'key': 'FFmpegSubtitlesConvertor',
            'format': 'srt',
        }],
        'writesubtitles': True,
        'postprocessor_hooks': [rename_postprocessor],
    }

    yt_dlp.YoutubeDL(ydl_opts).download([url])

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

# Example usage
rename_files_to_episode('D:/Casper/Temp', r'\bEP\d+\b')

# # Example usage
# url = "https://youtu.be/RRPBOCqO0wg?si=buIq84wpm8hQr9yj"
# # path = '/Users/liushiwen/Desktop/WINTERVACATION/output1.%(ext)s'
# path = 'D:/CASPER/output1%(title)s.%(ext)s'
# # ffmpeg_path = '/Users/liushiwen/Desktop/WINTERVACATION/ffmpeg'
# ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg.exe'
# download_video_srt(url, path, ffmpeg_path)
# # download_video_srt('https://www.youtube.com/watch?v=example', '/path/to/download', '/path/to/ffmpeg')
