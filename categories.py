from typing import NamedTuple, List

import db


class Category(NamedTuple):
    codename: str
    name: str
    aliases: List[str]


class Categories:

    def __init__(self):
        self.categories = self.all_category_from_db()

    @staticmethod
    def all_category_from_db() -> List[Category]:
        """Возвращает список категорий из бд """
        categories = db.fetchall(
            'category', 'codename name aliases'.split()
        )
        list_categories = []
        for category in categories:
            list_categories.append(Category(
                codename=category['codename'],
                name=category['name'],
                aliases=category['aliases']
            ))
        return list_categories

    def get_category(self, category_name):
        """Ищет и возвращает категорию по ее псевдониму"""
        result = None
        for category in self.categories:
            if category_name in category.aliases:
                result = category
        if not result:
            result = 'other'
        return result

    def get_all_category(self):
        """Возвращает список всех категорий"""
        return self.categories


if __name__ == '__main__':
    pass
