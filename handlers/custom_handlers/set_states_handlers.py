from loader import bot
from states.states import UserState


@bot.message_handler(commands=["base"])
def set_base_state(message):
    """Переход в обычный режим"""
    bot.set_state(message.from_user.id, UserState.base)
    bot.send_message(message.from_user.id, "Вы в стандартном режиме. Введите /help для просмотра команд")


@bot.message_handler(commands=["predict"])
def set_predict_state(message):
    """Переход в режим определения изображений"""
    bot.set_state(message.from_user.id, UserState.predict_state)
    bot.send_message(message.from_user.id, "Пришлите фотографию для того, чтобы бот её угадал. Введите /base для "
                                           "перехода в стандартный режим")

