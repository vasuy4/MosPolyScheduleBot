import time
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
            for day in all_day:
                if day:
                    day = day[0]
                    result += f"\nПредмет - {day["title"]}\nЛокация - {day["location"]} {day["rooms"][0] if len(day["rooms"]) > 0 else ""}"
            result += "\n\n"
    else:
        result = 'Введите название существующей группы.\nНапример, "/schedule 221-324"'

    for shift in range(0, len(result), 1000):
        bot.reply_to(message, result[shift:1000+shift])