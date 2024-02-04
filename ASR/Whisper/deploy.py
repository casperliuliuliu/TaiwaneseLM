import whisper

model = whisper.load_model("base")
result = model.transcribe("D:/Casper/Language/TaiwaneseLM/TOOLs/output.wav", language='zh-TW')
print(result["text"])