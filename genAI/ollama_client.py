# ollama_client.py
import requests

def query_ollama(prompt, model="gemma3"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "No response received.")
    else:
        return f"Error {response.status_code}: {response.text}"
