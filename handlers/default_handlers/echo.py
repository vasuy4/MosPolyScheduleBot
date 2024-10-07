from telebot.types import Message
from api.AI import ai_api
from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message):
    """Эхо хендлер, куда летят текстовые сообщения без указанного состояния"""
    bot.reply_to(message, ai_api.get_response(message.text)["result"] + ".\n*Если вы хотите воспользоваться функционалом бота, посмотрите список команд: /help")
