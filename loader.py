from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config
from models.predict_image_models.mospolytech_model import ModelMospolytech
import database.base_database

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
obj_model_mospolytech = ModelMospolytech()
