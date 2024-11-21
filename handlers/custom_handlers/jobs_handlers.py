from loader import bot

from telebot.types import Message
from typing import Dict, List, Optional

from api.jobs.jobs_api import get_jobs_response


userid_queryjob: Dict[int, str] = dict()


@bot.message_handler(commands=["set_query_job"])
def set_query_job(message: Message) -> None:
    """Хэндлер, меняющий искомую профессию"""
    words: List[str] = message.text.split()
    query_job: Optional[str] = " ".join(words[1:]) if len(words) > 1 else None
    if query_job:
        userid_queryjob[message.from_user.id] = query_job
        bot.reply_to(message, "Успешно задан запрос для поиска работы: " + query_job)
    else:
        bot.reply_to(message, 'Введите значение запроса искомой вакансии.\nНапример: "/set_query_job Web Developer"')

@bot.message_handler(commands=["jobs"])
def get_job_handler(message: Message) -> None:
    """Хэндлер, выводящий вакансию по запросу"""
    querystring: Dict[str, str] = {
        "query": userid_queryjob.get(message.from_user.id),
        "location":
    }
    if querystring["query"]:
        resp: dict = get_jobs_response(querystring)
        txt: str = ""
    else:
        bot.reply_to(message, 'Введите значение запроса искомой вакансии.\nНапример: "/set_query_job Web Developer"')