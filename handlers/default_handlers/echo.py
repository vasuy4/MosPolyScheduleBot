from telebot.types import Message

from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message):
    """Эхо хендлер, куда летят текстовые сообщения без указанного состояния"""
    bot.reply_to(
        message,
        f"Ваше сообщение: {message.text}\nПопробуйте написать что-то другое или выполнить команду (/help)",
    )
