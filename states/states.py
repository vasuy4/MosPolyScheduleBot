from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    """
    Состояния для пользователя
    """

    base = State()  # дефолтное состояние
    predict_cifar_state = State()  # состояние для определения изображений
    predict_mospolytech_state = State()  # состояние для определения адреса корпуса мосполитеха по изображению