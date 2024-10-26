from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    """Хэндлер, выводящий сообщение при запуске бота"""
    bot.reply_to(
        message,
        f"Здравствуйте, {message.from_user.full_name}! Я рад приветствовать вас! Я — бот, "
        f"который может предоставить информацию о расписании Московского Политеха и помочь вам определить объект на "
        f"фотографии. Для ознакомления с функционалом введите команду /help",
    )
