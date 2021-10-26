import sqlite3

conn = sqlite3.connect('db.db')
cursor = conn.cursor()


def insert(table, column_dict):
    columns = ', '.join(column_dict.keys())
    values = [tuple(column_dict.values())]
    placeholders = ', '.join('?' * len(column_dict.keys()))
    cursor.executemany(
        f"INSERT INTO {table}({columns}) VALUES({placeholders})", values)
    conn.commit()


def fetchall(table, columns_list):
    columns = ', '.join(columns_list)
    cursor.execute(f"SELECT {columns} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns_list):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete(table: str, expense_id: int):
    expense_id = int(expense_id)
    cursor.execute(f'DELETE FROM {table} where id={expense_id}')
    conn.commit()


def get_total_expenses(time, user_id):
    cursor.execute(f'SELECT sum(rubles) FROM expense where created>="{time}" '
                   f'and user="{user_id}"')
    result = cursor.fetchone()
    return result


def get_expenses_by_category_and_time(time, user_id):
    cursor.execute(f'SELECT  e.rubles, c.name '
                   f'FROM expense e LEFT JOIN category c '
                   f'on c.codename=e.category_codename '
                   f'WHERE e.created>="{time}" and e.user="{user_id}"')
    result = cursor.fetchall()
    return result


def get_last_expenses(user_id, count=10):
    cursor.execute(
        f'SELECT e.id, e.rubles, e.created, c.name '
        f'from expense  e  LEFT JOIN category c '
        f'on c.codename=e.category_codename WHERE e.user="{user_id}"'
        f'order by created desc limit {count}'
    )
    rows = cursor.fetchall()
    return rows


def init_db():
    with open('create_db.sql', 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


if __name__ == '__main__':
    init_db()
