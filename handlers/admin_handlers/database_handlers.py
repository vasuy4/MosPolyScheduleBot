from telebot.types import Message
from loader import bot
from config_data.config import ADMINS
from database.base_database import get_users


@bot.message_handler(commands=["users"])
def get_users_handler(message: Message):
    """Хэндлер, выводящий список пользователей бота"""
    if message.from_user.id in ADMINS:
        answer: str = ""
        for user in get_users():
            answer += "id: {}, name: {}\n".format(user.user_id, user.username)
        bot.reply_to(message, answer)
