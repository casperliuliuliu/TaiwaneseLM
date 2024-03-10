"""
Example code for yating tts api call.
"""
import sys
desired_path = "D:/Casper/Other"
sys.path.append(desired_path)
from my_config import get_config
config = get_config()
yating_key = config['yating_key']


from yating_tts_sdk import YatingClient as ttsClient

URL = "TTS_ENDPOINT"
URL = "https://tts.api.yating.tw/v2/speeches/short"
KEY = yating_key


TEXT = "歡迎收聽雅婷文字轉語音"
TEXT_TYPE = ttsClient.TYPE_TEXT
MODEL = ttsClient.MODEL_TAI_FEMALE_1
SPEED = 1.0
PITCH = 1.0
ENERGY = 1.5
ENCODING = ttsClient.ENCODING_MP3
SAMPLE_RATE = ttsClient.SAMPLE_RATE_16K
FILE_NAME = "example"

try:
    client = ttsClient(URL, KEY)
    client.synthesize(TEXT, TEXT_TYPE, MODEL, SPEED, PITCH, ENERGY, ENCODING, SAMPLE_RATE, FILE_NAME)
except Exception as err :
    print("An exception occurred:", err)