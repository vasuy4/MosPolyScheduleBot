from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    """
    Состояния для пользователя
    """
    base = State()  # дефолтное состояние
    predict_state = State()  # состояние для определения изображений