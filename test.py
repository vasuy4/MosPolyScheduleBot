from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot


def gen_markup():
    # Создаём объекты кнопок.
    button_1 = InlineKeyboardButton(text="Собаки 🦮", callback_data="dog")
    button_2 = InlineKeyboardButton(text="Кошки 🐈", callback_data="cat")

    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button_1, button_2)
    return keyboard


bot = TeleBot(
    "7952289391:AAHaNUDfeCN-rNGOwavu73Q-ESnSJK1UcaM"
)  # Токен, полученный от BotFather.


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.from_user.id,
        "Какое животное тебе нравится больше?",
        reply_markup=gen_markup(),  # Отправляем клавиатуру.
    )


@bot.callback_query_handler(
    func=lambda callback_query: (
        callback_query.data  # Обращаемся к callback_data, указанной при создании кнопки.
        == "dog"
    )
)
def dog_answer(callback_query):
    # Удаляем клавиатуру.
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    # Отправляем сообщение пользователю.
    bot.send_message(
        callback_query.from_user.id,
        "Я тоже люблю собак, они так мило машут хвостиком!",
    )


@bot.callback_query_handler(
    func=lambda callback_query: (
        callback_query.data  # Обращаемся к callback_data, указанной при создании кнопки.
        == "cat"
    )
)
def cat_answer(callback_query):
    # Удаляем клавиатуру.
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    # Отправляем сообщение пользователю.
    bot.send_message(
        callback_query.from_user.id,
        "Я тоже люблю кошек, они так умилительно мурлыкают!",
    )


bot.infinity_polling()
