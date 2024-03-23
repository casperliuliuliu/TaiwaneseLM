"""
Example code for yating tts api call.
"""
import sys
desired_path = "D:/Casper/Other"
# desired_path = "/Users/liushiwen/Desktop/大四下"

sys.path.append(desired_path)
from my_config import get_config
config = get_config()
yating_key = config['yating_key']
from yating_tts_sdk import YatingClient as ttsClient


def speak_word_with_yating(word, store_path = '', model_name=ttsClient.MODEL_TAI_FEMALE_1):
    URL = "TTS_ENDPOINT"
    URL = "https://tts.api.yating.tw/v2/speeches/short"
    KEY = yating_key

    TEXT = word
    TEXT_TYPE = ttsClient.TYPE_TEXT
    MODEL = model_name
    SPEED = 1.0
    PITCH = 1.0
    ENERGY = 1.5
    ENCODING = ttsClient.ENCODING_MP3
    SAMPLE_RATE = ttsClient.SAMPLE_RATE_16K
    FILE_NAME = store_path + '/' + word
    try:
        client = ttsClient(URL, KEY)
        client.synthesize(TEXT, TEXT_TYPE, MODEL, SPEED, PITCH, ENERGY, ENCODING, SAMPLE_RATE, FILE_NAME)
    except Exception as err :
        print("An exception occurred:", err)
    return FILE_NAME

if __name__ == "__main__":
    store_path = "/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/yating/"
    speak_word_with_yating("酷大便", store_path, ttsClient.MODEL_TAI_FEMALE_1)
    speak_word_with_yating("酷大便", store_path, ttsClient.MODEL_ZHEN_FEMALE_1)
