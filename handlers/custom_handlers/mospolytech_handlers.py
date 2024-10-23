import time
from datetime import datetime
from telebot.types import Message
from api.mospolytech.mospolytech_api import get_groups, get_schedule, get_now_week

from loader import bot
from keyboards.inline.mospolytech_inline import gen_markup_switch_groups, BORDERS_GROUPS

from typing import List, Optional, Union

GROUPS_CASH: List[Union[List[str], float]] = [
    [],
    time.time(),
]  # Кэширование списка групп


@bot.message_handler(commands=["groups"])
def bot_get_groups(message: Message):
    """Хэндлер, выводящий группы студентов."""
    if (
        not GROUPS_CASH[0] or time.time() - GROUPS_CASH[1] > 1800
    ):  # Обновление кэша каждые 30 мин.
        GROUPS_CASH[0] = get_groups()
        GROUPS_CASH[1] = time.time()
    bot.reply_to(
        message,
        "Список групп:\n"
        + ", ".join(GROUPS_CASH[0][BORDERS_GROUPS[0] : BORDERS_GROUPS[1]]),
        reply_markup=gen_markup_switch_groups(),
    )


@bot.message_handler(commands=["schedule"])
def bot_get_schedule(message: Message):
    """Хэнлер, выводящий расписание на текущую неделю для группы"""
    words: List[str] = message.text.split()
    group: Optional[str] = words[1] if len(words) > 1 else None
    if not GROUPS_CASH[0] or time.time() - GROUPS_CASH[1] > 1800:
        GROUPS_CASH[0] = get_groups()
        GROUPS_CASH[1] = time.time()
    result: List[str] = list()
    weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    if group in GROUPS_CASH[0]:
        schedule = get_schedule(group)
        week = get_now_week(schedule)
        result.append(f"*Расписание для группы {group}:*\n\n")
        for date, schedule_day in week["week"].items():
            day_str = f"===== {weekdays[datetime.strptime(date, '%d.%m.%Y').weekday()]} - {date} =====\n"
            for subject in schedule_day:
                day_str += f"*{subject['time'][0]}-{subject['time'][1]}*: {subject['subject']['title']}"
                rooms: Optional[str] = subject["subject"].get("rooms")
                link: Optional[str] = subject["subject"].get("link")
                if rooms:
                    day_str += "_ - " + " - ".join(rooms) + "_"
                elif link:
                    day_str += f" - {link}"
                day_str += "\n"
            if day_str[-2] == "=":
                day_str = ""
            else:
                day_str += "\n\n"
            if len(result[-1]) + len(day_str) < 1000:
                result[-1] += day_str
            else:
                result.append(day_str)

    else:
        result = [
            'Введите название существующей группы.\nНапример, "/schedule 221-324"'
        ]

    for messageField in result:
        for shift in range(0, len(messageField), 1000):
            bot.reply_to(
                message, messageField[shift : 1000 + shift], parse_mode="Markdown"
            )
