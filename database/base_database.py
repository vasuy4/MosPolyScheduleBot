from peewee import *
from config_data.config import DB_PATH
from telebot.types import Message
from peewee import IntegrityError


def table_exists(cursor, table_name):
    """Проверка на существование таблицы table_name в базе данных"""
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    # Если счёт равен 1, то таблица существует
    return cursor.fetchone()


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


if not User.table_exists():
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
            last_name=message.from_user.last_name
        )
        return True
    except IntegrityError:
        return False


if __name__ == "__main__":

    db.close()