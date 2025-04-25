import torch
from torch import nn
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
import os
import pandas as pd
from torchvision.io import read_image
from torchvision.io import ImageReadMode
import numpy as np
import torch
from transformers import AutoImageProcessor, AutoModel
from PIL import Image
import requests
from torch.utils.data import DataLoader
from flask import Flask, flash, request, redirect, url_for, session
from flask_cors import CORS, cross_origin
import json
import re
import base64
from io import BytesIO
from PIL import Image
from QuantumSelfAttentionLayer import QuantumSelfAttentionLayer

device = torch.device("cpu")

processor = AutoImageProcessor.from_pretrained('facebook/dinov2-base')
model = AutoModel.from_pretrained('facebook/dinov2-base').to(device)




class DiseaseClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_gelu_stack1 = nn.Sequential(
            nn.Linear(768, 512),
            nn.GELU(),
        )

        self.quantum = nn.Sequential(
            QuantumSelfAttentionLayer(512, 4, 5),
            nn.Linear(5, 512),
        )

        self.linear_gelu_stack2 = nn.Sequential(
            nn.Linear(512, 512),
            nn.GELU(),
            nn.Linear(512, 512),
        )

        self.linear_gelu_stack3 = nn.Sequential(
            nn.Linear(512, 512),
            nn.GELU(),
            nn.Linear(512, 9),
        )



    def forward(self, x):
        x = self.linear_gelu_stack1(x)
        x = x + self.quantum(x)
        x = x + self.linear_gelu_stack2(x)
        x = self.linear_gelu_stack3(x)
        return x


classifier = DiseaseClassifier().to(device)
classifier.load_state_dict(torch.load("quantum.pth", weights_only=True ), strict=False)

class DiseaseClassifierFull(nn.Module):
    def __init__(self, dino, processor, classifier):
        super().__init__()
        self.dino = dino
        self.classifier = classifier
        self.processor = processor

    def forward(self, x):
        inputs = self.processor(x, return_tensors="pt").to(device)
        outputs = self.dino(**inputs)
        values = self.classifier(torch.mean(outputs.last_hidden_state, axis=1))

        return torch.nn.functional.softmax(values)

detector = DiseaseClassifierFull(model, processor, classifier)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webp'])

app = Flask(__name__)
CORS(app)


app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xd9\xe3\x96.5\xd1\x01O<!\xd5\xb2\xa4\x9fR"\xa1\xa8'

# Function to check whether it is an alt girl
@app.route('/checkimage/', methods=['POST'])
@cross_origin()
def upload_file():
    # Get data
    data = request.data.decode('ascii')
    data = data[2:-2]
    parts = data.split(',')
    imageInfo = parts[0]
    imageData = parts[1]
    file_type = imageInfo.split(';')[0].split('/')[1]
    print(file_type)

    if file_type in ALLOWED_EXTENSIONS:
        print('Accepted file')
        # Decode the base64 image data
        decoded_image_data = bytearray(base64.decodebytes(imageData.encode('ascii')))
        byte_stream = BytesIO(decoded_image_data)
        image = Image.open(byte_stream)

        # Ensure the image has exactly 3 channels (RGB)
        image = image.convert("RGB")

        # Convert the PIL image to a PyTorch tensor
        image_tensor = ToTensor()(image)
        image_tensor = torch.tensor(image_tensor)*255

        # Convert the image to a NumPy array
        value = detector(image_tensor).detach().cpu().numpy().tolist()
        print("Value calculated")
        return {"value" : value}
    else:
        return {"error" : "Unsopported extension"}



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9400)
