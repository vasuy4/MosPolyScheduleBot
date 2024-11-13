from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS, ADMIN_COMMANDS
from loader import bot
from config_data.config import ADMINS


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    """Хэндлер, выводящий список команд, на которые реагирует бот"""
    if message.from_user.id in ADMINS:
        text = [f"/{command} - {desk}" for command, desk in ADMIN_COMMANDS]
    else:
        text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "Смотри, что я умею:\n" + "\n".join(text))
