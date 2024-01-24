import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_default_device("cuda")

model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype="auto", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
while True:
   content = input("Enter:")
   inputs = tokenizer( content, return_tensors="pt", return_attention_mask=False)

   outputs = model.generate(**inputs, max_length=200)
   text = tokenizer.batch_decode(outputs)[0]
   print(text)



# import torch
# from transformers import pipeline

# pipe = pipeline("text-generation", model="microsoft/phi-2", torch_dtype=torch.bfloat16, device_map="auto")
# while True:
#     content = input("Enter:")
#     # We use the tokenizer's chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
#     messages = [
#         {
#             "role": "system",
#             "content": "You are a friendly chatbot",
#         },

#         # {
#         #     "role": "user", 
#         #     "content": "How many helicopters can a human eat in one sitting?"
#         # },
#         {
#             "role": "user", 
#             "content": content
#         },
#     ]
#     prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
#     outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
#     print(outputs[0]["generated_text"])