import random
import json
import torch
from datetime import datetime
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize


import os
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

intents_path = os.path.join(BASE_DIR, "intents.json")
data_path = os.path.join(BASE_DIR, "data.pth")
logo_path = os.path.join(BASE_DIR, "logo.png")

with open(intents_path, "r", encoding="utf-8") as f:
    intents = json.load(f)



device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

FILE = 'data.pth'
data = torch.load(data_path, weights_only=False, map_location=torch.device('cpu'))

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "HappyMind"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])
                
                response = response.replace("{time}", datetime.now().strftime("%H:%M"))
                response = response.replace("{date}", datetime.now().strftime("%A, %d %B %Y"))
                
                return response
    return "I don't understand... Please ask something related to mental health."