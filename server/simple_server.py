from flask import Flask, request, jsonify, send_file
import os
app = Flask(__name__)

@app.route('/download_audio', methods=['GET'])
def download_audio():
    # Specify the path to your audio file
    audio_file_path = '/Users/liushiwen/Desktop/大四下/NSC/server/output.mp3'
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



