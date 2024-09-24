from telebot.types import Message
from api.mospolytech.api import get_groups
from loader import bot


@bot.message_handler(commands=["groups"])
def bot_get_groups(message: Message):
    """Хэндлер, выводящий группы студентов."""
    bot.reply_to(message, "Список групп:\n" + ", ".join(get_groups()[0:56]))

