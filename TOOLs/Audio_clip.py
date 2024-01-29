import pysrt
import wave
import contextlib
import os
import json

def srt_to_audio_clips(audio_file_path, srt_file_path, output_folder):
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

            output_file_path = os.path.join(output_folder, f"clip_{idx+1}.wav")
            
            with wave.open(output_file_path, 'wb') as output_audio:
                output_audio.setnchannels(audio.getnchannels())
                output_audio.setsampwidth(audio.getsampwidth())
                output_audio.setframerate(framerate)
                output_audio.writeframes(audio_clip)

            clips_to_subtitles[output_file_path] = [sub.text.replace('\n', ' ')]

    with open(os.path.join(output_folder, 'transcriptions.json'), 'w') as json_file:
        json.dump(clips_to_subtitles, json_file, indent=4)

    return clips_to_subtitles

if __name__ == "__main__":
    clips_transcriptions = srt_to_audio_clips("D:/CASPER/output1.wav", "D:/CASPER/output_test.srt", "D:/CASPER/Weight")
    print(json.dumps(clips_transcriptions, indent=4))
