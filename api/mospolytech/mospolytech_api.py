import json
import requests
from requests.exceptions import SSLError
from typing import List, Dict, Union, Tuple
from datetime import datetime, timedelta

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
TIME_SECTIONS = {
    "morning": [
        ["09:00", "10:30"],
        ["10:40", "12:10"],
        ["12:20", "13:50"],
        ["14:30", "16:00"],
        ["16:10", "17:40"],
        ["17:50", "19:20"],
        ["19:30", "21:00"],
    ],
    "evening": [
        ["09:00", "10:30"],
        ["10:40", "12:10"],
        ["12:20", "13:50"],
        ["14:30", "16:00"],
        ["16:10", "17:40"],
        ["18:20", "19:40"],
        ["19:50", "21:10"],
    ],
}


def make_request(url: str) -> Tuple[str, Union[SSLError, None]]:
    """Сделать запрос по ссылке для получения информации"""
    e = None
    try:
        r: requests.Response = requests.get(url=url, headers=HEADERS)
        content: str = r.content.decode("utf-8")
    except SSLError as e:
        content: str = ""

    return content, e


def parse_grid(grid_source: dict) -> List[list]:
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
    data, e = make_request(URLS["groups"])
    data = json.loads(data)
    return sorted(name for name in data["groups"])


def get_schedule(group: str) -> Dict[str, Union[list, str]]:
    is_session = False
    url: str = (
        URLS["schedule"]
        + f"?group={group.replace(' ', '%20')}&session={1 if is_session else 0}"
    )
    content, e = make_request(url)
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


def get_day(schedule: Dict[str, Union[list, str]], date: str) -> dict:
    """Возвращает словарь с расписанием указанного дня"""
    format_date: str = "%d.%m.%Y"
    d_date = datetime.strptime(date, format_date)
    grid = schedule["grid"]
    if len(grid) == 6:
        w = d_date.weekday()
        if w < 6:
            raw_day = grid[w]
        else:
            raw_day = [[] for _ in range(7)]
    else:
        d = abs((d_date - datetime.strptime(schedule["dates"][0], format_date)).days)
        raw_day = grid[d]

    day = {
        "group": schedule["group"],
        "type": schedule["type"],
        "is_session": schedule["is_session"],
        "date": date,
        "day": [],
    }

    for index, section in enumerate(raw_day):
        for raw_sbj in section:
            if (
                datetime.strptime(raw_sbj["dates"][0], format_date)
                <= datetime.strptime(date, format_date)
                <= datetime.strptime(raw_sbj["dates"][1], format_date)
            ):
                event = {
                    "time": TIME_SECTIONS[schedule["type"]][index],
                    "subject": dict(raw_sbj),
                }
                del event["subject"]["dates"]
                day["day"].append(event)
                break

    return day


def get_now_week(
    schedule: Dict[str, Union[list, str]]
) -> Dict[str, Union[dict, bool, str]]:
    """Возвращает словарь с расписанием текущей недели"""
    week = {
        "group": schedule["group"],
        "type": schedule["type"],
        "is_session": schedule["is_session"],
        "week": {},
    }
    date = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
    for i in range(6):
        new_day = get_day(schedule, date.strftime("%d.%m.%Y"))
        week["week"][new_day["date"]] = new_day["day"]
        date += timedelta(days=1)

    return week


if __name__ == "__main__":
    sch = get_schedule("221-324")
    # print(get_day(sch, datetime.now().date().strftime("%d.%m.%Y")))  # datetime.now().date().strftime("%d.%m.%Y")
    print(get_now_week(sch))
