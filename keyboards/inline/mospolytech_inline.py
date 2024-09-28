import telebot.types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from loader import bot


def gen_markup_switch_groups():
    """Создаёт инлайн-клавиатуру, переключающую списки групп"""
    button_back = InlineKeyboardButton(text="Назад⬅️", callback_data="back")
    button_forward = InlineKeyboardButton(text="Вперёд➡️", callback_data="forward")

    keyborad = InlineKeyboardMarkup()
    keyborad.add(button_back, button_forward)
    return keyborad


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "back"))
def back_answer(callback_query: CallbackQuery):
    """Коллбэк. Удаляет инлайн-кнопки и"""
    pass


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data == "forward")
)
def forward_answer(callback_query: CallbackQuery):
    """Коллбэк. Удаляет инлайн-кнопки и переключает список групп вперёд"""
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
