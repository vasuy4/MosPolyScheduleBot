from telebot.types import Message
from api.AI import ai_api
from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message):
    """Эхо хендлер, куда отправляются текстовые сообщения без указанного состояния"""
    if message.text.startswith("/"):
        bot.reply_to(message, "Для просмотра доступных команд введите /help")
    else:
        pass
        # bot.reply_to(
        #     message,
        #     ai_api.get_ai_response(message.text)["result"]
        #     + ".\n*Если вы хотите воспользоваться функционалом бота, посмотрите список команд: /help",
        # )
