from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from typing import List

from api.mospolytech.mospolytech_api import get_groups
from loader import bot


SHIFT_GROUP: int = 250
BORDERS_GROUPS: List[int] = [
    0,
    SHIFT_GROUP,
]  # Границы отображения групп для избежания переполнения длины сообщения


def gen_markup_switch_groups() -> InlineKeyboardMarkup:
    """Создаёт инлайн-клавиатуру, переключающую списки групп"""
    button_back = InlineKeyboardButton(text="Назад⬅️", callback_data="back")
    button_forward = InlineKeyboardButton(text="Вперёд➡️", callback_data="forward")

    keyborad = InlineKeyboardMarkup()
    keyborad.add(button_back, button_forward)
    return keyborad


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "back"))
def back_answer(callback_query: CallbackQuery) -> None:
    """Коллбэк. Удаляет инлайн-кнопки и сдвигает список групп назад"""
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    min_left_border: int = max(0, BORDERS_GROUPS[0] - SHIFT_GROUP)
    BORDERS_GROUPS[0] = min_left_border
    BORDERS_GROUPS[1] = min_left_border + SHIFT_GROUP
    groups: List[str] = get_groups()
    bot.reply_to(
        callback_query.message,
        "Список групп:\n" + ", ".join(groups[BORDERS_GROUPS[0] : BORDERS_GROUPS[1]]),
        reply_markup=gen_markup_switch_groups(),
    )


@bot.callback_query_handler(
    func=lambda callback_query: (callback_query.data == "forward")
)
def forward_answer(callback_query: CallbackQuery) -> None:
    """Коллбэк. Удаляет инлайн-кнопки и сдвигает список групп вперёд"""
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    groups: List[str] = get_groups()
    max_right_border: int = min(len(groups), BORDERS_GROUPS[1] + SHIFT_GROUP)
    BORDERS_GROUPS[0] = max_right_border - SHIFT_GROUP
    BORDERS_GROUPS[1] = max_right_border
    bot.reply_to(
        callback_query.message,
        "Список групп:\n" + ", ".join(groups[BORDERS_GROUPS[0] : BORDERS_GROUPS[1]]),
        reply_markup=gen_markup_switch_groups(),
    )
