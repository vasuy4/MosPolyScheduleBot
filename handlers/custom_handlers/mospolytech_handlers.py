import time
from datetime import datetime
from telebot.types import Message
from api.mospolytech.mospolytech_api import get_groups, get_schedule

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
    """Хэнлер, выводящий расписание для группы"""
    words: List[str] = message.text.split()
    group: Optional[str] = words[1] if len(words) > 1 else None
    if not GROUPS_CASH[0] or time.time() - GROUPS_CASH[1] > 1800:
        GROUPS_CASH[0] = get_groups()
        GROUPS_CASH[1] = time.time()
    result = ""
    if group in GROUPS_CASH[0]:
        schedule = get_schedule(group)
        result += f"Расписание для группы {group}:\n"
        for all_day in schedule["grid"]:
            now_pair = 0
            for day in all_day:
                if day:
                    day = day[0]
                    date1 = datetime.strptime(day['dates'][0].replace(".", "-"), "%d-%m-%Y")
                    date2 = datetime.strptime(day['dates'][1].replace(".", "-"), "%d-%m-%Y")
                    if date1 < datetime.now() < date2:
                        now_pair += 1
                        link: str = day.get('link')
                        result += f"\n{now_pair}) {day['title']}: {day['rooms'][0] if not link else link}"
            result += "\n==="
        result: List[str] = result.replace("' target='_blank'>📁 ПД</a>", "").split("===")
        result_full = [""]
        for day in result:
            if len(day) + len(result_full[-1]) < 1000:
                result_full[-1] += day
                continue
            result_full.append(day)
    else:
        result_full = ['Введите название существующей группы.\nНапример, "/schedule 221-324"']

    for messageField in result_full:
        for shift in range(0, len(messageField), 1000):
            bot.reply_to(message, messageField[shift:1000+shift])