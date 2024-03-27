from ailabs_asr.streaming import StreamingClient
import sys
from openai import OpenAI
from pydub import AudioSegment
import Levenshtein as lev
desired_path = "D:/Casper/Other"
desired_path = "/Users/liushiwen/Desktop/大四下/"
sys.path.append(desired_path)
from get_server_config import get_config
config = get_config()
yating_key = config['yating_key']
my_api_key = config["OPENAI_API_KEY"]

yating_result = ''
client = OpenAI(api_key=my_api_key)

def mp32wav(mp3_path,wav_path):
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")

def asr_from_whisper(audio_path, lang_code):
    audio_file= open(audio_path, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    language=lang_code
    )
    print(transcription.text)
    return transcription.text

def asr_from_yating(audio_path):
    global yating_result
    if audio_path[-3:] == "mp3":
         mp32wav(audio_path, audio_path[:-3]+"wav")
    audio_path = audio_path[:-3]+"wav"
    yating_result = ''
    asr_client = StreamingClient(yating_key)

    asr_client.start_streaming_wav(
    pipeline='asr-zh-tw-std',
    file=audio_path,
    verbose=False, 
    on_processing_sentence=on_processing_sentence,
    on_final_sentence=on_final_sentence)
    return yating_result

def on_processing_sentence(message):
    global yating_result
    yating_result += message["asr_sentence"]
    print(f'hello: {message["asr_sentence"]}')

def on_final_sentence(message):
    global yating_result
    yating_result = message["asr_sentence"]
    print(f'world: {message["asr_sentence"]}')

# def eval_yating(audio_path, ans_audio_path):
#     user_result = asr_from_yating(audio_path)
#     system_result = asr_from_yating(ans_audio_path)
    
def eval_whisper(user_audio_path, system_audio_path):  
    similarity_score = 0
    lang_list = ['ja', 'vi', 'id']
    scaling = 100 / len(lang_list)
    for lang_code in lang_list:
        user_result = asr_from_whisper(user_audio_path, lang_code)
        system_result = asr_from_whisper(system_audio_path, lang_code)
        similarity_score += string_similarity(user_result, system_result) * scaling
    return similarity_score

def string_similarity(str1, str2):
    distance = lev.distance(str1, str2)
    max_len = max(len(str1), len(str2))
    if max_len == 0:  
        return 1.0
    similarity = 1 - distance / max_len
    return similarity



if __name__ == "__main__":
    wav_path = "/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/server_audio/吃葡萄不吐葡萄皮，不吃葡萄，到吐葡萄皮。.wav"
    wav_path = "/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/yating/example.mp3"
    # print("real resul:", asr_from_yating(wav_path))
    # print("real resul:", asr_from_whisper(wav_path, 'vi'))
    user_audio_path = '/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/server_audio/蔡英文.mp3'
    system_audio_path = '/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/yating/example.mp3'
    # print(eval_whisper(user_audio_path, system_audio_path))
    print("result:",asr_from_yating("/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/server_audio/v3_audio.mp3"))