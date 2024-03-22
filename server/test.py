import requests
from ailabs_asr.streaming import StreamingClient
import sys
desired_path = "D:/Casper/Other"
desired_path = "/Users/liushiwen/Desktop/大四下/"
sys.path.append(desired_path)

from get_server_config import get_config
config = get_config()
yating_key = config['yating_key']

fileName = "your_file_path"

headers = {'key': yating_key}
files = {'file': open(fileName,'rb')}
response = requests.post('https://asr.api.yating.tw/v1/uploads',
                        headers=headers,
                        files=files)

print(response.json())


# fileName = "your_file_path"

# headers = {'key': yating_key}
# files = {'file': open(fileName,'rb')}
# response = requests.post('https://asr.api.yating.tw/v1/transcriptions',
#                         headers=headers,
#                         files=files)

# print(response.json())

import requests
import json

def post_transcription_request(audio_uri, api_key):
    url = "https://asr.api.yating.tw/v1/transcriptions"
    
    # Construct the request body
    payload = {
        "audioUri": audio_uri,
        "modelConfig": {
            "model": "asr-zh-en-std",
            "customLm": ""
        },
        "featureConfig": {
            "speakerDiarization": False,
            "speakerCount": 0,
            "sentiment": False,
            "punctuation": 0
        }
    }
    
    # Add headers including the API key for authorization
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Send the POST request
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        print("Request successful.")
        return response.json()  # Return the JSON response from the server
    else:
        print(f"Request failed with status code: {response.status_code}")
        return response.text  # Return the error message

# Example usage
audio_uri = "/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/server_audio/吃葡萄不吐葡萄皮，不吃葡萄，到吐葡萄皮。.wav"  # Replace with your actual audio URI
api_key = yating_key  # Replace with your actual API key
response = post_transcription_request(audio_uri, api_key)
print(response)
