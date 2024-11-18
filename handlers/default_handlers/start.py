from telebot.types import Message
from database.base_database import registration
from loader import bot
from config_data.config import ADMINS


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    """Хэндлер, выводящий сообщение при запуске бота"""
    is_new_user: bool = registration(message)
    if is_new_user:
        bot.reply_to(
            message,
            f"Здравствуйте, {message.from_user.full_name}! Я рад приветствовать вас! Я — бот, "
            f"который может предоставить информацию о расписании Московского Политеха и помочь вам определить объект на "
            f"фотографии. Для ознакомления с функционалом введите команду /help",
        )
    else:
        bot.reply_to(
            message,
            f"Рад вас снова видеть, {message.from_user.full_name}! Напомню, что я могу предоставить информацию о "
            f"расписании Московского Политеха и помочь вам определить объект на фотографии. "
            f"Для ознакомления с функционалом введите команду /help",
        )
