from data.loader import *
from data.confige import *
from key_boards.admin_key_boards import *
from services.api_sqlite import *
from aiogram.dispatcher import FSMContext
from aiogram import types

users = Users()
config = Config()


def is_admin(msg):
    return str(msg.from_user.id) in str(admins)


@dp.message_handler(is_admin, commands='admin')
async def admin_menu(message: types.Message):
    await message.answer('©Админ меню.', reply_markup=admin_action)


@dp.message_handler(is_admin, text='⚙️ Регулировка баланса')
async def balance_adjustment(message: types.Message):
    await message.answer("Введите ID пользователя, для которого хотите изменить баланс:",
                         reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Назад"))
    await storege.set_state(chat=message.from_user.id, state='user_balance')


@dp.message_handler(state='user_balance')
async def user_balance(message: types.Message, state: FSMContext):
    if message.text.capitalize() == "Назад":
        await message.answer('© Админ меню.', reply_markup=admin_action)
        await state.finish()
        return
    if not message.text.isdigit():
        await message.answer('Введите корректный чат ID пользователя!')
        return
    db_user = users.get_user(int(message.text))
    if db_user:
        await message.answer(f'Текущий баланс пользователя: {db_user["balance"]}')
        await message.answer('Введите новый баланс пользователя: ')
        await state.update_data(data={'chat_id': int(message.text)})
        await state.set_state(state='change_balance')
    else:
        await message.answer('ID юзера не найдено, введите корректные данные:')


@dp.message_handler(state='change_balance')
async def user_ban(message: types.Message, state: FSMContext):
    if message.text.capitalize() == "Назад":
        await message.answer('© Админ меню.', reply_markup=admin_action)
        await state.finish()
        return
    try:
        new_balance = abs(float(message.text))
        data =  await state.get_data()
        users.change_balance(data['chat_id'], new_balance)
        await message.answer('Данные были успешно изменены!')
        await message.answer('© Админ меню.', reply_markup=admin_action)
        await state.finish()
    except ValueError:
        await message.answer('Введите коректно данные!')
        return


@dp.message_handler(is_admin, text='❌ Бан Юзера')
async def ban_user_command(message: types.Message):
    await message.answer("Введите ID пользователя, которого нужно заблокировать или разблокировать:",
                         reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Назад"))
    await storege.set_state(chat=message.from_user.id, state='user_bun')


@dp.message_handler(state='user_bun')
async def user_ban(message: types.Message, state: FSMContext):
    if message.text.capitalize() == "Назад":
        await message.answer('© Админ меню.', reply_markup=admin_action)
        await state.finish()
        return
    if not message.text.isdigit():
        await message.answer('Введите корректный чат ID пользователя!')
        return
    db_user = users.get_user(int(message.text))
    if db_user:
        await message.answer(f'Текущий статус пользователя: {db_user["is_banned"]}')
        await message.answer('Что вы хотите сделать со статусом юзера?',
                            reply_markup=types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add('Забанить',
                                                                                      'Разбанить').add('Назад'))
        await state.update_data(data={'chat_id': int(message.text)})
        await state.set_state(state='bun_user_status')
    else:
        await message.answer('ID юзера не найдено, введите корректные данные:')


@dp.message_handler(state='bun_user_status')
async def user_ban(message: types.Message, state: FSMContext):
    if message.text.capitalize() == "Назад":
        await message.answer('© Админ меню.', reply_markup=admin_action)
        await state.finish()
        return
    else:
        data = await state.get_data()
        chat_id = data[list(data.keys())[0]]
        if message.text.capitalize() == 'Забанить':
            users.change_is_banned(chat_id, 1)
        elif message.text.capitalize() == 'Разбанить':
            users.change_is_banned(chat_id, 0)
        else:
            await message.answer('Введите коректные данные!')
            return
        await message.answer('Статус успешно изменен!')
        await message.answer('© Админ меню!', reply_markup=admin_action)
        await state.finish()


@dp.message_handler(text='🗒 Статистика')
async def static(message: types.Message):
    await message.answer(f'Количество юзеров: {len([user for user in users])}')







