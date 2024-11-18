from peewee import *
from config_data.config import DB_PATH
from telebot.types import Message
from peewee import IntegrityError
from typing import Iterable


db = SqliteDatabase(DB_PATH)
cursor = db.cursor()


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    """Класс пользователя"""

    user_id = IntegerField(primary_key=True)
    username = CharField()
    first_name = CharField()
    last_name = CharField(null=True)


if not User.table_exists():  # проверка и создание таблицы, если её нет.
    print("create table", User)
    db.create_tables([User])


def registration(message: Message) -> bool:
    """
    Регистрация нового пользователя
    Args:
        message (Message): данные от сообщения пользователя
    Returns:
        (bool): True при успешной регистрации. False - если пользователь уже зарегистрирован.
    """
    try:
        User.create(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        return True
    except IntegrityError:
        return False


def get_users() -> Iterable[User]:
    """
    Получить данные от телеграмм аккаунтов пользователей.
    """
    r = User.select()
    return r


if __name__ == "__main__":

    db.close()
