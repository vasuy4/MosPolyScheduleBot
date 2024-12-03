from loader import bot
from states.states import UserState


@bot.message_handler(commands=["base"])
def set_base_state(message):
    """Переход в обычный режим"""
    bot.set_state(message.from_user.id, UserState.base, message.chat.id)
    bot.send_message(
        message.from_user.id,
        "Вы в стандартном режиме. Введите /help для просмотра команд",
    )



@bot.message_handler(commands=["predict_address"])
def set_predict_mospolytech_state(message):
    """Переход в режим определения адреса корпуса Московского Политеха по изображению"""
    bot.set_state(
        message.from_user.id, UserState.predict_mospolytech_state, message.chat.id
    )
    bot.send_message(
        message.from_user.id,
        "Предоставьте изображение корпуса Московского Политеха, чтобы бот смог его идентифицировать. "
        "Для перехода в стандартный режим введите команду /base.",
    )
