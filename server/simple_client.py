import requests
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

def download_audio_from_server(base_url):
    url = base_url + "/download_audio"
    # The endpoint from where we want to download the audio
    response = requests.get(url)

    if response.status_code == 200:
        # Save the audio file received from the server
        filename = response.headers.get('Content-Disposition').split('filename=')[1].strip('"')
        with open("gogo"+filename, 'wb') as audio_file:
            audio_file.write(response.content)
        print(f'Audio file downloaded successfully: {"gogo"+filename}')
    else:
        print(f'Failed to download audio. Status code: {response.status_code}')

def send_message(base_url):
    url = base_url+"/post"
    headers = {'Content-Type': 'application/json'}
    message = {"message": "hey000\nggg123"}
    
    response = requests.post(url, json=message, headers=headers)
    
    if response.status_code == 200:
        print(f"Server response: {response.json()}")
    else:
        print("Failed to send message")

def send_message_and_audio(base_url, audio_file_path):
    url = base_url+"/upload_audio"  # Update with your actual server URL
    message = "This is a test message with audio."
    
    # Define the multipart/form-data payload
    payload = {
        'message': (None, message),  # None indicates no filename, as this part is text
    }
    files = {
        'audio': open(audio_file_path, 'rb')  # Open the audio file in binary read mode
    }
    
    # Make the POST request
    response = requests.post(url, files=files, data=payload)
    # Handle the response
    if response.status_code == 200:
        print(f"Server response: {response.json()}")
    else:
        print(f"Failed to send message and audio: {response.status_code}, {response.text}")

def record_audio(duration, fs, filename):

    print(f"Recording for {duration} seconds...")
    # Record audio for the given duration at the given sampling rate
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
    # Wait until the recording is finished
    sd.wait()
    # Save the recording as a WAV file
    write(filename, fs, np.int16(recording * 32767))
    print(f"Recording saved to {filename}")

if __name__ == "__main__":
    base_url = "https://511a-140-117-193-176.ngrok-free.app"
    # send_message(base_url)
    # record_audio(duration=3, fs=44100, filename='output.mp3')
    audio_file_path = "/Users/liushiwen/Desktop/大四下/NSC/server/output.mp3"  # Update this path to your audio file
    # send_message_and_audio(base_url, audio_file_path)
    download_audio_from_server(base_url)
