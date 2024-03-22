import requests
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import vlc
import time
def upload_image(base_url, image_path):
    url = base_url + "/upload_image"
    with open(image_path, 'rb') as image_file:
        # Define the request payload, including the file in the 'image' part
        files = {'image': (image_path, image_file)}
        # Make the POST request
        response = requests.post(url, files=files)
        # Check the response
        if response.status_code == 200:
            print("Image successfully uploaded.")
            print(response.json())  # Print the response message from the server
        else:
            print("Failed to upload image.")
            print(response.text)  # Print any error message from the server

def get_and_save_word_audio(base_url, word):
    url = base_url + "/speak_word"
    # Add the word as a query parameter
    params = {'word': word}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        filename = f"{word}.mp3"
        with open(filename, 'wb') as audio_file:
            audio_file.write(response.content)
        print(f"Audio file for '{word}' saved as {filename}")
    else:
        print(f"Failed to get audio for '{word}'. Server responded with status code {response.status_code}")

def play_stream(base_url):
    url = base_url + "/stream_audio"
    player = vlc.MediaPlayer(url)
    player.play()
    # Keep the script running while audio is playing
    while player.get_state() != vlc.State.Ended:
        time.sleep(1)

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
    base_url = "http://127.0.0.1:645"
    # send_message(base_url)
    # record_audio(duration=3, fs=44100, filename='output.mp3')

    # audio_file_path = "/Users/liushiwen/Desktop/大四下/NSC/server/output.mp3"  # Update this path to your audio file
    # # send_message_and_audio(base_url, audio_file_path)
    # play_stream(base_url)

    # get_and_save_word_audio(base_url, '眼藥水')
    upload_image(base_url, "/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/client_image/my_bro.png")
