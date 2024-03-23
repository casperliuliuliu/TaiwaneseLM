# pip install transformers>=4.34
# pip install accelerate

import torch
from transformers import pipeline
import sys
desired_path = "D:/Casper/Other"
sys.path.append(desired_path)
from my_config import get_config

config = get_config()
hf_token = config['Hugging_Face_Token']

path = "D:\Casper\OTHER\Weight\huggingface\hub\models--yentinglin--Taiwan-LLM-7B-v2.1-chat\snapshots\\be7d3a45160727c67088fda933c1413fa97138a2"

pipe = pipeline("text-generation", model=path, torch_dtype=torch.bfloat16, device_map="auto", token=hf_token)

while True:
    content = input("Enter:")
    # We use the tokenizer's chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
    messages = [
        {
            "role": "system",
            # "content": "你是一個人工智慧助理",
            "content": "你是一個介紹台灣文化與語言的小學老師，你知道台灣的地方特色，你在教學過程中會注意避免艱深晦澀的詞語。",
        },
        # {"role": "user", "content": "東北季風如何影響台灣氣候？"},
        {"role": "user", "content": content},
    ]
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    print(outputs[0]["generated_text"])
