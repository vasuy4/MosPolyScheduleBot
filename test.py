import requests

url = "https://open-ai21.p.rapidapi.com/claude3"

payload = {"messages": [{"role": "user", "content": "Привет!"}], "web_access": False}
headers = {
    "x-rapidapi-key": "4939550346msh30b7b1b9a8266c2p1653edjsnc859bbe3877e",
    "x-rapidapi-host": "open-ai21.p.rapidapi.com",
    "Content-Type": "application/json",
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())
