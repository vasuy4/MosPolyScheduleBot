import requests
import os

URL = "https://open-ai21.p.rapidapi.com/claude3"

payload = {"messages": [{"role": "user", "content": "Привет!"}], "web_access": False}
headers = {
    "x-rapidapi-key": os.getenv("API_AI_KEY"),
    "x-rapidapi-host": "open-ai21.p.rapidapi.com",
    "Content-Type": "application/json",
}

response = requests.post(URL, json=payload, headers=headers)

print(response.json())
