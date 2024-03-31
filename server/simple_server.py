from flask import Flask, request, jsonify, send_file, Response, stream_with_context, abort
import os
import random
from shutil import copyfile
from tts import speak_word_with_yating
import sys
import time
import werkzeug
from datetime import datetime
from eval_audio import eval_whisper, asr_from_yating
from pydub import AudioSegment
import server_function
desired_path = "/Users/liushiwen/Desktop/大四下/"
sys.path.append(desired_path)
from yating_tts_sdk import YatingClient as ttsClient

from get_server_config import get_config
config = get_config()
app = Flask(__name__)
# server_path = "D:\\Casper\\Language\\TaiwaneseLM\\server"
server_path = "/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/"
v1_answer_file_path = "/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/server_audio/v1_audio_l.mp3"
v2_answer_file_path = ""
v3_answer_file_path = ""
upload_audio_folder_path = f"{server_path}/server_audio/recordings/"
old_prompts = []
@app.route('/move_bawan', methods=['POST'])
def move_bawan():
    print("moving BaWan")
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing data"}), 400

    x = data.get('x')
    y = data.get('y')
    z = data.get('z')
    sausage_x = data.get('sausage_x')
    sausage_y = data.get('sausage_y')
    sausage_z = data.get('sausage_z')
    env  = {
        'x': x,
        'y': y,
        'z': z,
        'sausage_x': sausage_x,
        'sausage_y': sausage_y,
        'sausage_z': sausage_z,
    }
    print("BaWan x, y, z:",x, y, z)
    print("sausage x, y, z:",sausage_x, sausage_y, sausage_z)
    # instructions = {
    #     "moveX": 0.01,
    #     "moveY": 0.02,
    #     "moveZ": 0.03,
    #     "rotateX": 0.0,
    #     "rotateY": 1.0,
    #     "rotateZ": 0.0,
    #     "duration": 2  # Angle in degrees
    # }
    instructions = server_function.control_bot_llm(env)
    return jsonify(instructions)

@app.route('/v3_preparation', methods=['GET'])
def v3_preparation():
    print("Running v3_preparation")
    global v3_answer_file_path
    audio_names = ["v3_audio"]
    sentence_lists = [
        "一起學台語", 
        "我愛寫程式", 
        "吃飽沒",
        "最近好嗎？",
        "今天天氣怎麼樣",
        "食飽未？來食飯哦！",
    ]
    random_numbers = random.sample(range(0, len(sentence_lists)), 1)
    print("random choice:", random_numbers)
    selected_words = []
    for ii in range(1):
        store_path = f"{server_path}server_audio/{audio_names[ii]}"
        print(f"Storing Audio{ii} to {store_path}")
        selected_words.append(sentence_lists[random_numbers[ii]])
        speak_word_with_yating(sentence_lists[random_numbers[ii]], store_path, ttsClient.MODEL_TAI_FEMALE_1)
        
    ans_index = 0
    v3_sentence = selected_words[ans_index]
    v3_answer_file_path = f"{server_path}server_audio/{audio_names[ans_index]}.mp3"
    print(f"update v3 ans file to {v3_answer_file_path}")
    print(f"v3 sentence: {v3_sentence}")
    return jsonify({"response": v3_sentence})

@app.route('/v2_preparation', methods=['GET'])
def v2_preparation():
    print("Running v2_preparation")
    global v2_answer_file_path
    audio_names = ["v2_audio"]
    sentence_lists = [
        "吃西瓜不吐西瓜籽，不吃西瓜倒吐西瓜籽", 
        "一天一蘋果，醫生遠離我。", 
        "阿扁，錯了嗎？"
    ]
    random_numbers = random.sample(range(0, len(sentence_lists)), 1)
    print("random choice:", random_numbers)
    selected_words = []
    for ii in range(1):
        store_path = f"{server_path}server_audio/{audio_names[ii]}"
        print(f"Storing Audio{ii} to {store_path}")
        selected_words.append(sentence_lists[random_numbers[ii]])
        speak_word_with_yating(sentence_lists[random_numbers[ii]], store_path, ttsClient.MODEL_TAI_FEMALE_1)
        
    ans_index = 0
    v2_sentence = selected_words[ans_index]
    v2_answer_file_path = f"{server_path}server_audio/{audio_names[ans_index]}.mp3"
    print(f"update v2 ans file to {v2_answer_file_path}")
    print(f"v2 sentence: {v2_sentence}")
    return jsonify({"response": v2_sentence})

@app.route('/v1_eval', methods=['POST'])
def v1_eval():
    global v1_answer_file_path
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file part in the request"}), 400
    
    audio = request.files['audio']
    message = request.form.get('message', '')

    if audio.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if audio and message:
        # You can save the file to the server
        file_extension = werkzeug.utils.secure_filename(audio.filename).rsplit('.', 1)[1]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_filename = f"{timestamp}.{file_extension}"
        
        user_audio_path = os.path.join(upload_audio_folder_path, audio_filename)
        
        audio.save(user_audio_path)
        if file_extension == "m4a":
            audio = AudioSegment.from_file(user_audio_path, format="m4a")
            mp3_file_path = user_audio_path[:-3] + "mp3"
            # Export the audio to MP3
            audio.export(mp3_file_path, format="mp3")
            user_audio_path = mp3_file_path
        
        print(f"Received message: {message}")
        print(f"Audio saved to:\n{user_audio_path}")
        if message == "v1":
            ans_path = v1_answer_file_path
        elif message == "v2":
            ans_path = v2_answer_file_path
        elif message == "v3":
            ans_path = v3_answer_file_path
        if message == "main":
            print("talking to BaWan")
            asr_result = asr_from_yating(user_audio_path)
            store_path = f"{server_path}server_audio/main_audio"
            # asr_result = "什麼是水"
            print(f"Asr result:{asr_result}")
            llm_response = server_function.brain_llm(asr_result, old_prompts)
            print(f"BaWan:{llm_response}")
            speak_word_with_yating(llm_response, store_path, ttsClient.MODEL_TAI_FEMALE_1)
            old_prompts.append({"role": "user", "content": asr_result})
            old_prompts.append({"role": "assistant", "content": llm_response})
            while len(old_prompts) > 6:
                old_prompts.pop(0)
            return jsonify({"response": f"{llm_response}"})
        else:
            print(f"Ans file:\n{ans_path}")
            eval_score = eval_whisper(user_audio_path, ans_path)
            print(f"eval_score: {eval_score}")
            return jsonify({"response": f"{eval_score}"})
    else:
        return jsonify({"error": "Missing audio or message"}), 400


@app.route('/v1_download', methods=['GET'])
def v1_download():
    time.sleep(3)
    print("Running v1_download")
    text_input = request.args.get('text', None)
    if text_input is None:
        return "Missing text parameter", 400
    if text_input[-1] == "g":
        print(f"Sending image {text_input}")
        file_path = f'{server_path}server_image/{text_input}'
    else:
        print(f"Sending audio {text_input}")
        file_path = f'{server_path}server_audio/{text_input}'
    return send_file(file_path, as_attachment=True)


@app.route('/v1_preparation', methods=['GET'])
def v1_preparation():
    print("Running v1_preparation")
    global v1_answer_file_path
    audio_names = ["v1_audio_r", "v1_audio_m", "v1_audio_l"]
    img_names = ["v1_img_r", "v1_img_m", "v1_img_l"]
    word_lists = ["西瓜", "蘋果", "香蕉", "豆腐", "乾麵", "雞蛋", "茄子", "芒果", "南瓜", "草莓", "蘿蔔"]
    img_file = ["Watermelon", "Apple", "Banana", "Tofu", "Dry Noodles", "Egg", "Eggplant", "Mango", "Pumpkin", "Strawberry", "White Radish"]
    random_numbers = random.sample(range(0, len(word_lists)), 3)
    print("random choice:", random_numbers)
    selected_words = []
    for ii in range(3):
        store_path = f"{server_path}server_audio/{audio_names[ii]}"
        print(f"Storing Audio{ii} to {store_path}")
        selected_words.append(word_lists[random_numbers[ii]])
        speak_word_with_yating(word_lists[random_numbers[ii]], store_path, ttsClient.MODEL_TAI_FEMALE_1)
        
        source_path = f"{server_path}/server_image/v1_{img_file[random_numbers[ii]]}.png"
        destination_path = f"{server_path}/server_image/{img_names[ii]}.png"
        print(f"Storing Image{ii} to {destination_path}")
        copyfile(source_path, destination_path)

    ans_index = random.sample(range(0, len(selected_words)), 1)
    v1_answer = selected_words[ans_index[0]]
    v1_answer_file_path = f"{server_path}server_audio/{audio_names[ans_index[0]]}.mp3"
    print(f"v1 answer:{v1_answer}")
    return jsonify({"response": v1_answer})

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
    audio_file_path = f"{server_path}server_audio/main_audio.mp3"
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
    app.run(debug=True, host='0.0.0.0', port=45216)



