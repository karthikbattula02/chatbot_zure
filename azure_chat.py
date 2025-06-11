import os
import requests
from dotenv import load_dotenv

load_dotenv()

def ask_azure(prompt):
    url = f"{os.getenv('AZURE_ENDPOINT')}openai/deployments/{os.getenv('AZURE_DEPLOYMENT_NAME')}/chat/completions?api-version={os.getenv('AZURE_API_VERSION')}"
    headers = {
        "api-key": os.getenv("AZURE_API_KEY"),
        "Content-Type": "application/json"
    }
    body = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        res = requests.post(url, headers=headers, json=body)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error contacting Azure API: {e}"
