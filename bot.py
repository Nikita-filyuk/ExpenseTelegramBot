import logging
from aiogram import Bot, Dispatcher, executor, types

import exceptions
from config import TOKEN
from expenses import *
from services import get_time_start

API_TOKEN = TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Отправляет Приветственное сообщение"""
    await message.answer(f'Добро пожаловать, {message.from_user.first_name}\n'
                         f'Вас приветсвует бот для учета расходов.\n'
                         f'Если нужна помощь /help\n',
                         reply=False)


@dp.message_handler(commands=['last'])
async def last_of_expenses(message: types.Message):
    """Отправляет последние 10 трат с возможностью удаления"""
    expenses = get_last_expenses(message.from_user.id)
    last_expenses_rows = [
        f'{expense.rubles} руб. на {expense.category_name}'
        f' в {expense.created}  для удаления /delete{expense.id}'
        for expense in expenses]
    answer_message = 'Последние сохраненные траты: \n\n' + '\n\n'.join(
        last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """Отправляет инстукцию по боту"""
    await message.answer('Чтобы добавить трату:\n'
                         'Еда 200\n'
                         'Чтобы узнать список категорий: /categories\n'
                         'Получение статистики:\n'
                         '/day - за сегодня\n'
                         '/month - за месяц\n'
                         '/year - за год.',
                         reply=False)


@dp.message_handler(commands=['categories'])
async def get_all_categories(message: types.Message):
    """Отправляет список всех категорий"""
    result = Categories().categories
    categories = [cat.name for cat in result]
    answer_message = 'Существующие категории:\n' + '\n'.join(categories)
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/delete'))
async def delete_expenses(message: types.Message):
    """Удаляет трату по ее id"""
    expense_id = int(message.text[7:])
    delete_expense(expense_id)
    await message.answer(f'Трата {expense_id} успешно удалена')


@dp.message_handler(commands=['day'])
async def statistic_of_day(message: types.Message):
    """Отпрвляет суточная статистику трат по категориям"""
    time = get_time_start()
    expenses = get_statistic_by_categories(time['day'], message.from_user.id)
    total = get_total_expenses(time['day'], message.from_user.id)
    expense_list = [f'{expense.category_name}: {expense.rubles}руб.'
                    for expense in expenses]
    answer_message = 'Всего потрачено сегодня: \n\n' + '\n\n'.join(
        expense_list)
    await message.answer(answer_message + f'\n\nОбщее: {total}руб. ')


@dp.message_handler(commands=['month'])
async def statistic_of_month(message: types.Message):
    """Отпрвляет месячную статистику трат по категориям"""
    time = get_time_start()
    expenses = get_statistic_by_categories(time['month'], message.from_user.id)
    total = get_total_expenses(time['month'], message.from_user.id)
    print(total)
    expense_list = [f'{expense.category_name}: {expense.rubles}руб.'
                    for expense in expenses]
    answer_message = 'Всего потрачено за месяц: \n\n' + '\n\n'.join(
        expense_list)
    await message.answer(answer_message + f'\n\nОбщее: {total}руб. ')


@dp.message_handler(commands=['year'])
async def statistic_of_year(message: types.Message):
    """Отпрвляет годовую статистику трат по категориям"""
    time = get_time_start()
    expenses = get_statistic_by_categories(time['year'], message.from_user.id)
    total = get_total_expenses(time['year'], message.from_user.id)
    expense_list = [f'{expense.category_name}: {expense.rubles}руб.'
                    for expense in expenses]
    answer_message = 'Всего потрачено за год: \n\n' + '\n\n'.join(
        expense_list)
    await message.answer(answer_message + f'\n\nОбщее: {total}руб. ')


@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавляет трату"""
    try:
        expense = add_expenses(message.text, message.from_user.id)
    except exceptions.WrongMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f'Добавлены траты {expense.rubles} руб '
        f'на {expense.category_name}.\n\n')
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
