import time
from telebot.types import Message
from api.mospolytech.mospolytech_api import get_groups

from loader import bot
from keyboards.inline.mospolytech_inline import gen_markup_switch_groups, BORDERS_GROUPS

from typing import List, Optional, Union

GROUPS_CASH: List[Union[List[str], float]] = [[], time.time()]  # Кэширование списка групп


@bot.message_handler(commands=["groups"])
def bot_get_groups(message: Message):
    """Хэндлер, выводящий группы студентов."""
    if not GROUPS_CASH[0] or time.time() - GROUPS_CASH[1] > 1800:  # Обновление кэша каждые 30 мин.
        print("new")
        GROUPS_CASH[0] = get_groups()
        GROUPS_CASH[1] = time.time()
    print(time.time() - GROUPS_CASH[1])
    bot.reply_to(
        message,
        "Список групп:\n" + ", ".join(GROUPS_CASH[0][BORDERS_GROUPS[0] : BORDERS_GROUPS[1]]),
        reply_markup=gen_markup_switch_groups(),
    )

@bot.message_handler(commands=["schedule"])
def bot_get_schedule(message: Message):
    """Хэнлер, выводящий расписание для группы"""
    group: Optional[str] = message.text.split()[1] if len(message.text) > 1 else None

