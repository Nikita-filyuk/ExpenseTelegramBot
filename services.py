import re
from datetime import datetime
from typing import Dict, NamedTuple

from exceptions import WrongMessage


class Message(NamedTuple):
    rubles: int
    category: str


def parse_message(message) -> Message:
    """ Парсит сообщение и возвращает Message """
    rubles = re.search(r'\d+', message)
    category = re.search(r'\D+', message)
    if not rubles or not category:
        raise WrongMessage(
            'Кажется, я не смог понять ваше сообщение. '
            'Необходимо указать название категории и сумму')
    rubles = int(rubles.group(0).replace(' ', ''))
    category = category.group().lower().replace(' ', '')
    return Message(rubles=rubles, category=category)


def get_now_datetime() -> str:
    """Возвращает форматированное время"""
    return datetime.now().strftime('%d-%m-%y %H:%M:%S')


def get_time_start() -> Dict:
    """
    Возвращает форматированное начало периода для статистики.
    Пример year: 01-01-21

    """
    now = datetime.now()
    day = f'{now.day}-{now.month}-{now.year}'
    month = f'01-{now.month}-{now.year}'
    year = f'01-01-{now.year}'
    time = {
        'day': day,
        'month': month,
        'year': year
    }
    return time
