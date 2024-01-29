from pydub import AudioSegment
import os
def sum_audio_durations(folder_path):
    total_duration = 0
    # AudioSegment.converter = r"C:/ffmpeg/bin/ffmpeg.exe"  # Update this path as needed

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a')):  # Add other formats if needed
            audio_path = os.path.join(folder_path, filename)
            audio = AudioSegment.from_file(audio_path)
            total_duration += len(audio)

    return total_duration / 1000  # Convert milliseconds to seconds

def convert_seconds(total_seconds):
    time_components = []
    days = total_seconds // (24 * 3600)
    if days > 0:
        time_components.append(f"{int(days)} day")

    total_seconds = total_seconds % (24 * 3600)
    hours = total_seconds // 3600
    if hours > 0:
        time_components.append(f"{int(hours)} hr")

    total_seconds %= 3600
    minutes = total_seconds // 60
    if minutes > 0:
        time_components.append(f"{int(minutes)} min")

    seconds = total_seconds % 60
    if seconds > 0:
        time_components.append(f"{seconds:.1f} sec")

    formatted_time = " ".join(time_components)
    print(formatted_time)



if __name__ == "__main__":
    folder_path = 'D:/Casper/Weight/test'
    total_duration_seconds = sum_audio_durations(folder_path)
    convert_seconds(total_duration_seconds)
