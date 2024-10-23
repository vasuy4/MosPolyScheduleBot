from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config
from models.cifar.cifar_model import Model as AI_Model


storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
model = AI_Model()
