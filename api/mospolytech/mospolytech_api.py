import json
import requests
from typing import List

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/86.0.4240.75 Safari/537.36"
)
URLS = {
    "referer": "https://rasp.dmami.ru/",
    "groups": "https://rasp.dmami.ru/groups-list.json",
}
HEADERS = {"referer": URLS["referer"], "user-agent": DEFAULT_USER_AGENT}


def make_request(url: str) -> str:
    """Сделать запрос по ссылке для получения информации"""
    r: requests.Response = requests.get(url=url, headers=HEADERS)
    content: str = r.content.decode("utf-8")
    return content


def get_groups() -> List[str]:
    """Получить группы студентов"""
    data = json.loads(make_request(URLS["groups"]))
    return sorted(name for name in data["groups"])


if __name__ == "__main__":
    print("Список студентов:\n" + ", ".join(get_groups()))
