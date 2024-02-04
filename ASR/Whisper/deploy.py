import whisper

model = whisper.load_model("base")
result = model.transcribe("D:/Casper/OTHER/Weight/test/clip_19.wav", language='zh')
print(result["text"])