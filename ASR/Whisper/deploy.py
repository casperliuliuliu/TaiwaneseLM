import whisper

model = whisper.load_model("base")
result = model.transcribe("D:/Casper/Weight/clip_1.wav")
print(result["text"])