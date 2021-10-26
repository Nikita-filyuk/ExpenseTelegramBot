from typing import NamedTuple, Optional, List

import db
import services
from categories import Categories


class Statistic(NamedTuple):
    rubles: int
    category_name: str


class Expense(NamedTuple):
    id: Optional[int]
    rubles: int
    created: str
    category_name: str


def get_total_expenses(time: str, user_id: int):
    """Возвращает сумму всех трат за выбранный период"""
    row = db.get_total_expenses(time, user_id)
    if row:
        return row[0]
    return 0


def get_statistic_by_categories(time: str, user_id: int) -> List[Statistic]:
    """Возвращает статистику по категориям и времени"""
    categories = Categories().get_all_category()
    rows = db.get_expenses_by_category_and_time(time, user_id)
    dict_row = {}
    for cat in categories:
        dict_row[cat.name] = 0
        for obj in rows:
            if cat.name == obj[1]:
                dict_row[cat.name] += obj[0]
    statistic = [
        Statistic(rubles=obj[1], category_name=obj[0]) for obj in
        dict_row.items() if obj[1] > 0
    ]
    return statistic


def add_expenses(message: str, user_id: str) -> Expense:
    """Добавляет трату и возвращает Expense"""
    parsed_messages = services.parse_message(message)
    category = Categories().get_category(parsed_messages.category)
    rubles = parsed_messages.rubles
    db.insert('expense', {
        'rubles': rubles,
        'created': services.get_now_datetime(),
        'category_codename': category.codename,
        'user': user_id,
        'message': message
    })
    return Expense(id=None, rubles=rubles, category_name=category.name,
                   created='')


def get_last_expenses(user_id: str) -> List[Expense]:
    """Возращает последние 10 трат"""
    rows = db.get_last_expenses(user_id)
    last_expenses = [
        Expense(id=row[0], rubles=row[1], category_name=row[3], created=row[2])
        for row in rows]
    return last_expenses


def delete_expense(expense_id: int):
    """Удаляет трату по его id"""
    db.delete('expense', expense_id)


if __name__ == '__main__':
    pass
