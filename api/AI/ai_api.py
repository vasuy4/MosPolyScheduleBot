import requests
from config_data.config import AI_API_KEY

URL = "https://open-ai21.p.rapidapi.com/claude3"

example_payload = {
    "messages": [{"role": "user", "content": "Привет!"}],
    "web_access": False,
}
headers = {
    "x-rapidapi-key": AI_API_KEY,
    "x-rapidapi-host": "open-ai21.p.rapidapi.com",
    "Content-Type": "application/json",
}


def get_ai_response(text: str) -> dict:
    """Получить ответ ИИ на сообщение"""
    payload = {"messages": [{"role": "user", "content": text}], "web_access": False}
    response = requests.post(URL, json=payload, headers=headers)
    return response.json()


if __name__ == "__main__":
    response = requests.post(URL, json=example_payload, headers=headers)
    print(response.json())
    print(response.json()["result"])
