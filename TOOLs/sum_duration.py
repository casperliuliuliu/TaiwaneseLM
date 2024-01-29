from pydub import AudioSegment
import os
def sum_audio_durations(folder_path):
    total_duration = 0
    AudioSegment.converter = r"C:/ffmpeg/bin/ffmpeg.exe"  # Update this path as needed

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a')):  # Add other formats if needed
            audio_path = os.path.join(folder_path, filename)
            audio = AudioSegment.from_file(audio_path)
            total_duration += len(audio)

    return total_duration / 1000  # Convert milliseconds to seconds

if __name__ == "main":
    folder_path = 'D:/Casper/Weight/test'
    total_duration_seconds = sum_audio_durations(folder_path)
    print(f"Total audio duration: {total_duration_seconds} seconds")
