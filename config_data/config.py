import json
import os
from dotenv import load_dotenv, find_dotenv
from json import loads


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

DB_PATH = "database.sqlite"
BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
AI_API_KEY = os.getenv("API_AI_KEY")
JOBS_API_KEY = os.getenv("API_KEY")
ADMINS = loads(os.getenv("ADMINS"))
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("groups", "Вывести список групп"),
    ("schedule", "Вывести расписание группы"),
    ("base", "Переход в стандартный режим"),
    (
        "predict_address",
        "Переход в режим определения адресов корпуса Московского Политеха по изображению",
    ),
)

ADMIN_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("groups", "Вывести список групп"),
    ("schedule", "Вывести расписание группы"),
    ("base", "Переход в стандартный режим"),
    (
        "predict_address",
        "Переход в режим определения адресов корпуса Московского Политеха по изображению",
    ),
)
