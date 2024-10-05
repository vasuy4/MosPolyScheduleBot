import json
import requests
from typing import List, Dict, Union, Any
from get_type_annotations.get_type_annotations import get_type_annotation

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/86.0.4240.75 Safari/537.36"
)
URLS = {
    "referer": "https://rasp.dmami.ru/",
    "groups": "https://rasp.dmami.ru/groups-list.json",
    "schedule": "https://rasp.dmami.ru/site/group",
}
HEADERS = {"referer": URLS["referer"], "user-agent": DEFAULT_USER_AGENT}


def make_request(url: str) -> str:
    """Сделать запрос по ссылке для получения информации"""
    r: requests.Response = requests.get(url=url, headers=HEADERS)
    content: str = r.content.decode("utf-8")
    return content


def parse_grid(grid_source: dict) -> list[list]:
    # creating modified grid
    grid_modified = []
    for key_i in grid_source:
        day = []
        for key_j in grid_source[key_i]:
            section = []
            for obj in grid_source[key_i][key_j]:
                # preparing link for event
                link = obj["e_link"]
                if link is None:
                    dirty_link = obj["auditories"][0]["title"]
                    if dirty_link[0:7] == "<a href":
                        link = dirty_link[9:].split('"')[0]
                # preparing dates for event
                if len(key_i) == 10:
                    dates = [".".join(d.split("-")[::-1]) for d in [key_i] * 2]
                else:
                    dates = [
                        ".".join(d.split("-")[::-1]) for d in [obj["df"], obj["dt"]]
                    ]
                # creating event
                event = {
                    "title": obj["sbj"].strip(),
                    "type": obj["type"],
                    "teachers": [
                        " ".join(t.strip().split()) for t in obj["teacher"].split(",")
                    ],
                    "location": obj["location"].strip(),
                    "rooms": [r.strip().replace("_", "") for r in obj["shortRooms"]],
                    "link": link,
                    "dates": dates,
                }
                # clearing event fields
                event["teachers"] = list(filter(lambda t: t != "", event["teachers"]))
                # appending
                section.append(event)
            day.append(section)
        grid_modified.append(day)

    # returning modified grid
    return grid_modified


def get_groups() -> List[str]:
    """Получить группы студентов"""
    data = json.loads(make_request(URLS["groups"]))
    return sorted(name for name in data["groups"])


def get_schedule(group: str) -> Dict[str, Union[list, str]]:
    is_session = False
    url: str = (
        URLS["schedule"]
        + f"?group={group.replace(' ', '%20')}&session={1 if is_session else 0}"
    )
    content: str = make_request(url)
    data: Dict[str, Union[str, dict]] = json.loads(content)
    schedule = {
        "group": group,
        "type": "evening" if data["group"]["evening"] else "morning",
        "is_session": data["isSession"],
        "dates": [
            ".".join(d.split("-")[::-1])
            for d in [data["group"]["dateFrom"], data["group"]["dateTo"]]
        ],
        "grid": parse_grid(data["grid"]),
    }
    return schedule


if __name__ == "__main__":
    sch = get_schedule("221-324")
