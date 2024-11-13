from telebot.types import Message
from loader import bot
from config_data.config import ADMINS


@bot.message_handler(commands=["users"])
def get_users_handler(message: Message):
    """Хэндлер, выводящий список пользователей бота"""
    bot.reply_to(message, "test")