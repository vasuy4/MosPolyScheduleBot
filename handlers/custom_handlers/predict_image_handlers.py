from loader import bot, obj_model_mospolytech
from models.predict_image_models.base_model import BasePredictModel
from states.states import UserState
import os

from telebot.types import Message, File
from typing import Dict

translate: Dict[str, str] = {
    # cifar
    "airplane": "самолёт",
    "automobile": "автомобиль",
    "bird": "птица",
    "cat": "кошка",
    "deer": "олень",
    "dog": "собака",
    "frog": "лягушка",
    "horse": "лошадь",
    "ship": "корабль",
    "truck": "грузовик",
    # mospolytech
    "Б_Семёновская_38": "ул. Б. Семёновская, д. 38",
    "Прянишникова_2а": "ул. Прянишникова, 2А",
    "Автозаводская_16": "ул. Автозаводская, д. 16",
}


def predict_img(message: Message, obj_model: BasePredictModel) -> None:
    """Передача информации для модели и ответ пользователю"""
    if message.photo:
        file_id: str = message.photo[-1].file_id
        file_info: File = bot.get_file(file_id)
        file_path: str = file_info.file_path

        # Скачиваем файл
        downloaded_file: bytes = bot.download_file(file_path)

        # Сохраняем файл на диск
        cache_path: str = os.path.join("cache", f"{file_id}.jpg")
        with open(cache_path, "wb") as new_file:
            new_file.write(downloaded_file)
        answer: str = obj_model.predict_image(cache_path)

        bot.reply_to(message, "Так это же: " + translate.get(answer, answer))
        os.remove(cache_path)
    else:
        bot.reply_to(
            message, "Предоставьте, пожалуйста, изображение для идентификации объекта"
        )



@bot.message_handler(state=UserState.predict_mospolytech_state, content_types=["photo"])
def predict_mospolytech_image_handler(message: Message) -> None:
    """Хэндлер, угадывающий с помощью ИИ адрес корпуса Политеха по картинке"""
    predict_img(message, obj_model_mospolytech)


@bot.message_handler(content_types=["photo"])
def get_image_handler(message: Message) -> None:
    if message.photo:
        bot.reply_to(
            message,
            "В рамках работы с изображениями доступны следующие команды:\n"
            "/predict_address - переход в режим определения адреса корпуса Московского Политеха по "
            "изображению",
        )
