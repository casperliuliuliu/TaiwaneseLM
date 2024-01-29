import torch
import torch.nn as nn
import torchaudio

class SimpleASRModel(nn.Module):
    def __init__(self, num_classes=32):
        super(SimpleASRModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=(3, 3), stride=(2, 2))
        self.rnn = nn.GRU(input_size=32, hidden_size=128, num_layers=2, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(128 * 2, num_classes)  # num_classes depends on your dataset

    def forward(self, x):
        x = self.conv1(x)
        x, _ = self.rnn(x)
        x = self.fc(x)
        return x
    
def preprocess_audio(audio_path):
    waveform, sample_rate = torchaudio.load(audio_path)
    # Convert to spectrogram
    spectrogram = torchaudio.transforms.Spectrogram()(waveform)
    return spectrogram


import string

# Basic characters: lowercase letters and space
basic_chars = list(string.ascii_lowercase) + [' ']

# Add any extra characters you need
extra_chars = ['\'', '.', ',', '?']  # Add punctuation as needed

# Total number of classes
num_classes = len(basic_chars) + len(extra_chars) + 1  # +1 for end-of-sentence token

print("Number of classes:", num_classes)


from torchaudio.datasets import LIBRISPEECH
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

librispeech_dataset = LIBRISPEECH("./data", url="train-clean-100", download=True)
import torchaudio
from torchaudio.transforms import MelSpectrogram, Resample

# Define transformations
transform = torchaudio.transforms.Compose([
    Resample(orig_freq=16000, new_freq=8000),  # Resample from 16kHz to 8kHz
    MelSpectrogram(),  # Convert to Mel-Spectrogram
])

# Applying transformations to the dataset
transformed_dataset = [(transform(waveform), label) for waveform, _, _, label, _, _ in librispeech_dataset]

# transform = transforms.Compose([
#     transforms.ToTensor(),
#     transforms.Normalize((0.5,), (0.5,))
# ])


# # Create the DataLoader for our training set
train_loader = DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)
for epoch in range(num_epochs):
    for data in train_loader:
        waveform, sample_rate, utterance, speaker_id, chapter_id, utterance_id = data
        # Your training code here

# model = SimpleASRModel()
# criterion = nn.CTCLoss()
# optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# for epoch in range(num_epochs):
#     for i, (audio, labels, input_lengths, label_lengths) in enumerate(train_loader):
#         optimizer.zero_grad()
#         output = model(audio)
#         loss = criterion(output, labels, input_lengths, label_lengths)
#         loss.backward()
#         optimizer.step()



