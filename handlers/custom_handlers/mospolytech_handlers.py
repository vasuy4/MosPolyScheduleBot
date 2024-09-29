from telebot.types import Message
from api.mospolytech.mospolytech_api import get_groups

from loader import bot
from keyboards.inline.mospolytech_inline import gen_markup_switch_groups, BORDERS_GROUPS

from typing import List


@bot.message_handler(commands=["groups"])
def bot_get_groups(message: Message):
    """Хэндлер, выводящий группы студентов."""
    groups: List[str] = get_groups()
    bot.reply_to(
        message,
        "Список групп:\n" + ", ".join(groups[BORDERS_GROUPS[0] : BORDERS_GROUPS[1]]),
        reply_markup=gen_markup_switch_groups(),
    )
