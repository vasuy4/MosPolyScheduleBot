import requests
import os

URL = "https://open-ai21.p.rapidapi.com/claude3"

example_payload = {"messages": [{"role": "user", "content": "Привет!"}], "web_access": False}
headers = {
    "x-rapidapi-key": os.getenv("API_AI_KEY"),
    "x-rapidapi-host": "open-ai21.p.rapidapi.com",
    "Content-Type": "application/json",
}


def get_response(text: str) -> dict:
    """Получить ответ на сообщение"""
    payload = {"messages": [{"role": "user", "content": text}], "web_access": False}
    response = requests.post(URL, json=payload, headers=headers)
    return response.json()


if __name__ == "__main__":
    response = requests.post(URL, json=example_payload, headers=headers)
    print(response.json())
    print(response.json()["result"])