from transformers import pipeline
import torch

# Initialize the pipeline with your model
path = "D:\Casper\OTHER\Weight\huggingface\hub\models--HuggingFaceH4--zephyr-7b-beta\snapshots\dc24cabd13eacd3ae3a5fe574bd645483a335a4a"
pipe = pipeline("text-generation", model=path, torch_dtype=torch.bfloat16, device_map="auto")

# Initialize an empty string to store conversation history
conversation_history = ""

def ask_llm(question, max_history_length=1024):
    global conversation_history
    # Concatenate the question to the conversation history
    prompt = conversation_history + "\n" + question
    
    # Generate a response
    response = pipe(prompt)[0]['generated_text'][len(prompt):]  # Extract only the new response
    
    # Update the conversation history with the question and the generated response
    conversation_history += "\n" + question + "\n" + response
    
    # If necessary, truncate the conversation history to the last max_history_length characters
    conversation_history = conversation_history[-max_history_length:]
    
    return response

# Example usage
user_input = input("Enter:")
while user_input != "q":
    response = ask_llm(user_input)
    print(response)
    user_input = input("Enter:")

# print(response)
