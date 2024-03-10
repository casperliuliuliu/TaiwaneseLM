# Install transformers from source - only needed for versions <= v4.34
# pip install git+https://github.com/huggingface/transformers.git
# pip install accelerate
# In[]
import torch
from transformers import pipeline
path = "D:\Casper\OTHER\Weight\huggingface\hub\models--HuggingFaceH4--zephyr-7b-beta"
path = "D:\Casper\OTHER\Weight\huggingface\hub\models--HuggingFaceH4--zephyr-7b-beta\snapshots\dc24cabd13eacd3ae3a5fe574bd645483a335a4a"
pipe = pipeline("text-generation", model=path, torch_dtype=torch.bfloat16, device_map="auto")
conversation_history = []

# while True:
content = input("Enter:")
# We use the tokenizer's chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
messages = [
    {
        "role": "system",
        "content": "You are a friendly chatbot",
    },
    {
        "role": "user", 
        "content": content
    },
]
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
# In[]
print(outputs[0]["generated_text"])
# print(dir(outputs[0]["generated_text"][0]))
# <|system|>
# You are a friendly chatbot who always responds in the style of a pirate.</s>
# <|user|>
# How many helicopters can a human eat in one sitting?</s>
# <|assistant|>
# Ah, me hearty matey! But yer question be a puzzler! A human cannot eat a helicopter in one sitting, as helicopters are not edible. They be made of metal, plastic, and other materials, not food!

# %%
print(output[0]["generated_text"][0])
# %%
