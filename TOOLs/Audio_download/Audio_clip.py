import pysrt
import wave
import contextlib
import os
import json

def srt_to_audio_clips(audio_file_path, srt_file_path, output_folder, output_prefix):
    subs = pysrt.open(srt_file_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    clips_to_subtitles = {}

    with contextlib.closing(wave.open(audio_file_path, 'rb')) as audio:
        framerate = audio.getframerate()
        for idx, sub in enumerate(subs):
            start = sub.start.ordinal / 1000
            end = sub.end.ordinal / 1000
            audio.setpos(int(start * framerate))
            frame_count = int((end - start) * framerate)
            audio_clip = audio.readframes(frame_count)
            output_filename = f"{output_prefix}_{idx+1}.wav"
            output_file_path = os.path.join(output_folder, output_filename)
            
            with wave.open(output_file_path, 'wb') as output_audio:
                output_audio.setnchannels(audio.getnchannels())
                output_audio.setsampwidth(audio.getsampwidth())
                output_audio.setframerate(framerate)
                output_audio.writeframes(audio_clip)

            clips_to_subtitles[output_filename] = [sub.text.replace('\n', ' ')]

    with open(os.path.join(output_folder, 'transcriptions.json'), 'w', encoding='utf-8') as json_file:
        json.dump(clips_to_subtitles, json_file, indent=4, ensure_ascii=False)

    os.remove(audio_file_path)
    os.remove(srt_file_path)

    return clips_to_subtitles

if __name__ == "__main__":
    clips_transcriptions = srt_to_audio_clips("D:/CASPER/output1.wav", "D:/CASPER/output1.en.srt", "D:/Casper/Weight/test2", "hello")
    print(json.dumps(clips_transcriptions, indent=4))
