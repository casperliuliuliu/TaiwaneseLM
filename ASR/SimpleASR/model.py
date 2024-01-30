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
        x = x.permute(2, 1, 0)  # Reshaping for RNN; new shape: (batch_size, time_steps, 32, features_after_conv)
        x = x.reshape(x.size(0), x.size(1), -1)  # Flatten the last two dimensions for RNN; new shape: (batch_size, time_steps, flattened_features)
        x, _ = self.rnn(x)
        x = self.fc(x)
        return x

import string

# Basic characters: lowercase letters and space
basic_chars = list(string.ascii_lowercase) + [' ']

# Add any extra characters you need
extra_chars = ['\'', '.', ',', '?']  # Add punctuation as needed

# Total number of classes
num_classes = len(basic_chars) + len(extra_chars) + 1  # +1 for end-of-sentence token

print("Number of classes:", num_classes)


# from torchaudio.datasets import LIBRISPEECH
# from torch.utils.data import DataLoader
# from torchvision import datasets, transforms

# librispeech_dataset = LIBRISPEECH("./data", url="train-clean-100", download=True)
# import torchaudio
# from torchaudio.transforms import MelSpectrogram, Resample

# resampler = Resample(orig_freq=16000, new_freq=8000)  # Resample from 16kHz to 8kHz
# melspectrogramer =  MelSpectrogram()  # Convert to Mel-Spectrogram

# train_loader = DataLoader(dataset=librispeech_dataset, batch_size=1, shuffle=True)

# for audio, labels, input_lengths, label_length, ii, jj in train_loader:
#     print(audio.shape)
#     data = resampler(audio)
#     data = melspectrogramer(data)
#     print(data.shape)

#     break
# model = SimpleASRModel()
# criterion = nn.CTCLoss()
# optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# print(model)
# num_epochs = 5
# for epoch in range(num_epochs):
#     for i, (audio, labels, input_lengths, label_lengths, ii, jj) in enumerate(train_loader):
#         optimizer.zero_grad()

#         data = resampler(audio)
#         data = melspectrogramer(data)
#         output = model(data)

#         loss = criterion(output, labels, input_lengths, label_lengths)
#         loss.backward()
#         optimizer.step()



import torch
import torchaudio
from torchaudio.datasets import LIBRISPEECH
from torchaudio.transforms import MelSpectrogram, Resample
from torch.utils.data import DataLoader
from torch.nn import CTCLoss
from torch.optim import Adam
import torch.nn as nn


# Load the dataset
librispeech_dataset = LIBRISPEECH("./data", url="train-clean-100", download=True)

# Transforms
resampler = Resample(orig_freq=16000, new_freq=8000)  # Resample from 16kHz to 8kHz
melspectrogramer = MelSpectrogram(n_mels=32)  # Convert to Mel-Spectrogram

# Data Loader
train_loader = DataLoader(dataset=librispeech_dataset, batch_size=1, shuffle=True)

# Instantiate model, loss function, and optimizer
model = SimpleASRModel()
criterion = CTCLoss()
optimizer = Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 5
for epoch in range(num_epochs):
    for i, (audio, labels, input_lengths, label_lengths, i, j) in enumerate(train_loader):
        print(i)
        print(j)
        print(label_lengths)
        optimizer.zero_grad()

        # Preprocessing
        audio = audio.squeeze(1)  # Remove channel dimension
        data = resampler(audio)
        data = melspectrogramer(data)
        # Forward pass
        output = model(data)
#         # Adjusting shapes for CTCLoss; output shape -> (T, N, C)
        output = output.permute(2, 0, 1)  # Assuming model's output is (N, C, T)
        print(len(output.shape))
        
#         # Loss and backpropagation
        ## Loss function STILL got problems.
        loss = criterion(output, labels, torch.tensor(output.shape[0], dtype=torch.int8), label_lengths)
        # loss.backward()
#         optimizer.step()

#     print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}")

# print("Training completed")
