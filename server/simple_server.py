from flask import Flask, request, jsonify, send_file, Response, stream_with_context
import os
from yating.yating_tts import speak_word_with_yating
import sys
desired_path = "/Users/liushiwen/Desktop/大四下/"
sys.path.append(desired_path)

from get_server_config import get_config
config = get_config()
app = Flask(__name__)

# app.config = config

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No image part in the request'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'message': 'No image selected for uploading'}), 400
    if file:
        # Optionally, save the file to your server
        filepath = os.path.join(config['UPLOAD_FOLDER'], "img.png")
        # print(file.filename)
        file.save(filepath)
        # Respond to the client
        return jsonify({'message': 'Image successfully received'}), 200
    
@app.route('/speak_word')
def speak_word():
    # Get the word from query parameters, e.g., /speak_word?word=hello
    word = request.args.get('word', '')
    if not word:
        return "No word provided", 400
    store_path = "/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/server_audio"
    filename = speak_word_with_yating(word, store_path)
    path_to_file = os.path.join('audio_files', f"{filename}.mp3")
    if not os.path.exists(path_to_file):
        return "Failed to generate audio", 500
    
    return send_file(path_to_file, as_attachment=True)

def stream_audio(file_path):
    with open(file_path, "rb") as audio_file:
        while chunk := audio_file.read(4096):  # Read in 4KB chunks
            yield chunk

@app.route('/stream_audio')
def stream_audio_route():
    audio_file_path = '/Users/liushiwen/Desktop/大四下/output1.mp3'
    # audio_file_path = '/Users/liushiwen/Desktop/大四下/output1.wav'
    # audio_file_path = "/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/server_audio/output.mp3"
    return Response(stream_with_context(stream_audio(audio_file_path)), content_type="audio/wav")

@app.route('/download_audio', methods=['GET'])
def download_audio():
    # Specify the path to your audio file
    audio_file_path = '/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/server_audio/output.mp3'
    return send_file(audio_file_path, as_attachment=True)

@app.route('/upload_audio', methods=['POST']) # This function could be streaming
def receive_audio():
    # Check if the post request has the file part
    if 'audio' not in request.files:
        return jsonify({"response": "No audio part in the request"}), 400
    
    audio = request.files['audio']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if audio.filename == '':
        return jsonify({"response": "No selected file"}), 400
    
    if audio:
        audio_save_path = '/Users/liushiwen/Desktop/大四下/NSC/server/audio'
        os.makedirs(audio_save_path, exist_ok=True)
        audio_path = os.path.join(audio_save_path, audio.filename)
        
        audio.save(audio_path)
        print(f"Received and saved audio file: {audio.filename}")
        message = request.form['message']
        print(f"Received message: {message}")
        return jsonify({"response": "Audio uploaded successfully!"})
    
@app.route('/post', methods=['POST'])
def receive_message():
    message = request.json['message']
    print(f"Received message: {message}")
    return {"response": "Message received successfully!"}

@app.route('/get', methods=['GET'])
def send_message():
    # Predefined message to send back to the client
    response_message = {"response": "Hello from server, this is captain Casper"}
    return jsonify(response_message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=645)



