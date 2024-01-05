# pip install transformers>=4.34
# pip install accelerate

import torch
from transformers import pipeline
import sys
desired_path = "D:/Casper/"
sys.path.append(desired_path)
from my_config import get_config

config = get_config()
hf_token = config['Hugging_Face_Token']


pipe = pipeline("text-generation", model="yentinglin/Taiwan-LLM-7B-v2.1-chat", torch_dtype=torch.bfloat16, device_map="auto", token=hf_token)

# We use the tokenizer's chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
messages = [
    {
        "role": "system",
        "content": "你是一個人工智慧助理",
    },
    {"role": "user", "content": "東北季風如何影響台灣氣候？"},
]
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
print(outputs[0]["generated_text"])
