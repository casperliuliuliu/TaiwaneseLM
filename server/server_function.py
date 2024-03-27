import sys
import base64
import requests
from openai import OpenAI
desired_path = "/Users/liushiwen/Desktop/大四下/"
sys.path.append(desired_path)
from get_server_config import get_config
config = get_config()
my_api_key = config["OPENAI_API_KEY"]
client = OpenAI(api_key=my_api_key)


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def vision_llm(image_path):
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            # {"type": "text", "text": "What's in this image?"},
            {"type": "text", "text": "這張照片中有什麼東西？"},
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            },
            },
        ],
        }
    ],
    max_tokens=300,
    )
    return response.choices[0]

def completion_llm(message, old_prompt):
    
    prompt = [
        # {"role": "system", "content": "You are an elementary teacher. "},
        # {"role": "system", "content": "你是一個小學老師，現在正在陪伴一位同學聊天，用口語以及繁體中文的方式做出回覆，因為同學的輸入是以語音辨識後的文字輸入，可能會有許多奇怪斷點及錯字，因此請盡力推測同學所表達的意思，並基於此作出回答。"},
        {"role": "system", "content": "You are an elementary school teacher currently engaging in a chat with a student. Please respond using colloquial language and Traditional Chinese characters. Since the student's input is through voice recognition, there may be unusual breaks and misspellings in the text. Therefore, try your best to infer the intended meaning of the student's messages and respond accordingly."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125", # cheaper
    messages=prompt
    )
    memory_summary(prompt[-1]['content'])
    message = response.choices[0].message.content
    return message

def prompting(message, old_prompt):
    
    prompt = [
        # {"role": "system", "content": "You are an elementary teacher. "},
        # {"role": "system", "content": "你是一個小學老師，現在正在陪伴一位同學聊天，用口語以及繁體中文的方式做出回覆，因為同學的輸入是以語音辨識後的文字輸入，可能會有許多奇怪斷點及錯字，因此請盡力推測同學所表達的意思，並基於此作出回答。"},
        {"role": "system", "content": "You are an elementary school teacher currently engaging in a chat with a student. Please respond using colloquial language and Traditional Chinese characters. Since the student's input is through voice recognition, there may be unusual breaks and misspellings in the text. Therefore, try your best to infer the intended meaning of the student's messages and respond accordingly."}
    ]
    memory_prompt = fetch_memory()
    prompt.append(memory_prompt)

    prompt += old_prompt
    message_prompt = {"role": "user", "content": message}
    prompt.append(message_prompt)

    # fetch_memory
    return prompt


def control_bot_llm(env_prompt): # return json file to control functions
    action_json = ''
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to control a robot by outputing JSON."},
        {"role": "user", "content": env_prompt}
    ]
    )
    print(response.choices[0].message.content)
    return action_json

def fetch_memory():
    return "hehe"

def memory_summary(prompt): # access txt 
    # re
    return 1

def brain_llm(prompt, vision_flag=False, img_path=''):
    vision_message = ""
    if vision_flag :
        vision_message = vision_llm(img_path)

    text_message = ''

    response = client.chat.completions.create(
    # model="gpt-3.5-turbo",
    model="gpt-3.5-turbo-0125", # cheaper
    messages=prompt
    )
    memory_summary(prompt[-1]['content'])
    return response.choices[0].message.content

def translating(english_message): # might not use this.
    chinese_message = ''
    return chinese_message


def generate_image(gen_img_prompt):
    response = client.images.generate(
    model="dall-e-2",
    prompt=gen_img_prompt,
    size="256x256",
    quality="standard",
    n=1,
    )
    image_url = response.data[0].url
    return image_url

def download_image(image_url, image_name):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_name, 'wb') as file:
            file.write(response.content)
        print(f"Image successfully downloaded: {image_name}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

def evaluation(audio_path):

    score = 100
    return score


def pretend_move(xx, yy, zz):
    if len(xx) != len(yy):
        return -1
    elif len(xx) != len(zz):
        return -1
    for ii in range(len(xx)):
        print(f"x:{xx[ii]}, y:{yy[ii]}, z:{zz[ii]}")

def pretend_spin(xx_angle, yy_angle, zz_angle):
    if len(xx_angle) != len(yy_angle):
        return -1
    elif len(xx_angle) != len(zz_angle):
        return -1
    for ii in range(len(xx_angle)):
        print(f"x:{xx_angle[ii]}, y:{yy_angle[ii]}, z:{zz_angle[ii]}")

def pretend_send_env():
    env_prompt = {
        'curr_xx' : 20,
        'curr_yy' : 0,
        'curr_zz' : 20,
        'curr_xx_angle' : 0,
        'curr_yy_angle' : 0,
        'curr_zz_angle' : 0,

        'BaWan_xx': 155, # None for no food now
        'BaWan_yy': 0, 
        'BaWan_zz': 200, 
    }


if __name__ == "__main__":
    img_path = "/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/server_image/img.png"
    img_path = "/Users/liushiwen/Desktop/大四下/NSC/TaiwaneseLM/server/server_image/"
    # vision_message = vision_llm(img_path)
    # print(vision_message)

    # gen_img_prompt = "a cartoon fruit"
    # generate_image(gen_img_prompt)

    # brain_llm('hello')
    # Example prompt
    # prompt = "Given the current position is (0, 0, 0) and orientation is (0, 0, 0), where should the AR object move if it wants to approach the target located at (5, 5, 0)?"

    # print(control_bot_llm(prompt))

    # food_list = ["芒果", "雞蛋", "綠豆", "蘋果", "蘿蔔", "茄子", "南瓜", "西瓜", "豆腐", "乾麵"]
    food_list = ["Mango", "Egg", "Mung Bean", "Apple", "Radish", "Eggplant", "Pumpkin", "Watermelon", "Tofu", "Dry Noodles"]
    food_list = ["Eggplant", "Pumpkin", "Watermelon", "Tofu", "Dry Noodles"]
    food_list = ["White Radish", "Banana", "Chinese Tofu", "Chinese Fried Rice", "Strawberry"]

    for food in food_list:
        prompt = f"a cartoon style pixel art of {food}"
        url = generate_image(prompt)
        download_image(url, f"{img_path}{food}.png")
        # break