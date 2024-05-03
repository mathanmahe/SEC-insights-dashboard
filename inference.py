import requests
import os

def query(payload, model_id, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-ru-en"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

model_id = "distilbert-base-uncased"
api_token = os.getenv("HF_TOKEN")
# data = query("The goal of life is [MASK].", model_id, api_token)

file_path = "clean/sec-edgar-filings/AAPL/10-K/0000320193-17-000070/full-submission.txt"

with open(file_path, 'r') as file:
    text = file.read()

print(len(text.split()))


data = query({"inputs": text}, model_id, api_token)
print(data)