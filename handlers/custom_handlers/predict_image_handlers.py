from loader import bot, model
from states.states import UserState
from telebot.types import Message
import os


@bot.message_handler(state=UserState.predict_state, content_types=["photo"])
def predict_image_handler(message: Message):
    """Хэндлер, угадывающий существо на изображении"""
    if message.photo:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        # Скачиваем файл
        downloaded_file = bot.download_file(file_path)

        # Сохраняем файл на диск
        cache_path = os.path.join("cache", f"{file_id}.jpg")
        with open(cache_path, "wb") as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Ваше существо: " + model.predict_image(cache_path))
        os.remove(cache_path)
    else:
        bot.reply_to(message, "Пришлите фотографию для определения существа")
