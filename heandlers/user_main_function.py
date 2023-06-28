from key_boards.user_key_boards import *
from data.loader import *
from data.confige import *
from aiogram.dispatcher import FSMContext
from aiogram import types
from services.api_sqlite import *
import asyncio
from os import path
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

users = Users()
config = Config()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    if not users.get_user(message.from_user.id):
        ref = message.get_args()
        if ref:
            if users.get_user(ref):
                users.add_user(message.from_user.username, message.from_user.id, ref)
            else:
                users.add_user(message.from_user.username, message.from_user.id)
        else:
            users.add_user(message.from_user.username, message.from_user.id)

    member_1 = await bot.get_chat_member(mains_channels_id, message.from_user.id)
    member_2 = await bot.get_chat_member(mains_chat_id, message.from_user.id)
    status = ["member", "administrator", "creator"]
    if member_1.status not in status or member_2.status not in status:
        main_menu_1 = InlineKeyboardMarkup(row_width=1).add(
             InlineKeyboardButton('Подписатся на канал ', url=mains_channels),
             InlineKeyboardButton('Подписатся на чат', url=mains_chat),
             InlineKeyboardButton('Продолжить', callback_data='check_subscribe'))
        await message.answer_photo(caption='▪Для начала работы с ботом, пройдите небольшую\nпроверку, просто '
                                           'вступите в <a href="https://t.me/+FW2NiVVDnR82ZDUy">чат</a>'
                                           ' и <a href="https://t.me/investment_canal">канал</a> ниже и нажмите\n'
                                           'кнопку продолжить.\n\n'
                                           '©️ Нажмите на «Подписаться 1 и 2»', parse_mode='html',
                                   photo=types.InputFile(path.join('img', 'authorization.jpeg')),
                                   reply_markup=main_menu_1)
    else:
        await message.answer('© Главное меню.', reply_markup=user_menu)


@dp.callback_query_handler(text='check_subscribe')
async def continue_menu(call: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)
    member = await bot.get_chat_member(chat_id=mains_channels_id, user_id=call.from_user.id)
    if member.status in ["member", "administrator", "creator"]:
        member2 = await bot.get_chat_member(chat_id=mains_chat_id, user_id=call.from_user.id)
        if member2.status in ["member", "administrator", "creator"]:
            await call.message.answer('©️ Главное меню.', reply_markup=user_menu)
            return
    await call.message.answer('⬆ Подпишитесь на чат/канал ⬆')  # окошко делает show_alert=True


@dp.message_handler(text='📞 Контакты')
async def process_contacts(message: types.Message):
    await message.answer('📧 Добро пожаловать в наш раздел контактной информации платформы:\n'
                                  'Служба поддержки: @ZX8support\n'
                                  'Наш сайт: В разработке')


@dp.message_handler(text="🗓 Обучения")
async def study_investment(message: types.Message):
    contact = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton('➕ Открыть обучение', url='https://telegra.ph/Obuchenie-BNB-04-20'))
    await message.answer_photo(caption='🎓 Попал в бота, но не знаешь, что делать? Тогда ознакомься\n'
                                       'с нашим минутным обучением:',
                               photo=types.InputFile(path.join('img', 'education (1).jpeg')),
                               reply_markup=contact)


@dp.message_handler(text="🗓 Обучения", state="*")
async def process_state_learn(msg: types.Message, state: FSMContext):
    await study_investment(msg)
    await state.finish()


@dp.message_handler(text='⌨ Калькулятор')
async def calc_investment(message: types.Message):
    await message.answer(text='▪ Введите сумму, которую хотите рассчитать:',
                         reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Назад"))
    await storege.set_state(chat=message.chat.id, state='calculate')


@dp.message_handler(state='calculate')
async def calculate_investment(message: types.Message, state: FSMContext):
    if message.text.lower() == 'назад':
        await message.answer('© Главное меню.', reply_markup=user_menu)
        await state.finish()
        return
    try:
        amount = float(message.text)
        if amount <= 100:
            raise ValueError
        percent = config.get_percent()

        daily_return = amount * percent / 100
        monthly_return = daily_return * 30.4167
        yearly_return = daily_return * 365
        await message.answer_photo(caption='💱 В данном разделе Вы сумеете рассчитать Вашу прибыль, от суммы вашей '
                                           'инвестиции в наш проект:\n\n'
                                           f'💵 Ваша инвестиция: {amount}\n'
                                           f'Прибыль в сутки: {daily_return}\n'
                                           f'Прибыль в месяц: {monthly_return}\n'
                                           f'Прибыль в год: {yearly_return}', photo=types.InputFile(path.join('img',
                                                                    'calculator.jpeg')),
                                   reply_markup=types.InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(
                                       '➕ Рассчитать повторно', callback_data='calculate_again'
                                   )))

        await state.finish()
    except ValueError:
        await message.answer('🚫 Минимальная сумма инвестиции 100.0₽, введите корректную сумму!')
        return


@dp.callback_query_handler(text='calculate_again')
async def calculate_again_1(call: types.CallbackQuery):
    await call.message.answer(text='▪ Введите сумму, которую хотите рассчитать:',
                         reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Назад"))
    await storege.set_state(chat=call.message.chat.id, state='calculate')


@dp.message_handler(text="⌨ Калькулятор", state="*")
async def process_state_calc(msg: types.Message, state: FSMContext):
    await calc_investment(msg)
    await state.finish()


@dp.message_handler(text='👔 Партнерам')
async def user_partners(message: types.Message):
    me = await bot.get_me()
    await message.answer_photo(caption='▪ Партнерская программа создана для того чтобы получить клиенту'
                                       'дополнительный источник дохода, приглашайте людей по своей ссылке\n\n'
                                       f'💸 Процент с инвестиций: {investmen}%\n'
                                       f'💳 Всего заработано: {users.get_user(message.from_user.id)["investments"]}\n\n'
                                       f'👥 Партнеров: {users.get_count_ref(message.from_user.id)} \n\n'
                                       f'🔗 Ваша реф-ссылка:\nhttps://t.me/{me.username}'
                                       f'?start={message.from_user.id}\n\n'
                                       f'〽 Внешняя реф-ссылка:\nhttps://teleg.run/{me.username}'
                                       f'?start={message.from_user.id}\n\n', photo=types.InputFile(path.join('img',
                                                  'partners.jpeg')),
                                       reply_markup=types.InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(
                                       "➕ Как набрать партнеров", url='https://telegra.ph/Partnyoram-BNB-04-20'
                                       )))


@dp.message_handler(text="👔 Партнерам", state="*")
async def process_state_partners(msg: types.Message, state: FSMContext):
    await user_partners(msg)
    await state.finish()


@dp.message_handler(text='💳 Кошелек')
async def process_state_wallet(message: types.Message):
    user = users.get_user(message.from_user.id)
    partners = len([user for user in users if str(user['is_ref']) == str(message.from_user.id)])
    await message.answer_photo(caption= f'🤖 Ваш ID: {message.from_user.id}\n'
                               f'📆 Профиль создан: {user["date_created"]}\n\n'
                               f'💳 Ваш баланс: {user["balance"]}₽\n'
                               f'👥 Партнеров: {partners}чел.\n\n',
                               photo=types.InputFile(path.join('img', 'wallet.jpeg')),
                               reply_markup=types.InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(
                                   "➕ Пополнить", callback_data="top_up"),
                                   InlineKeyboardButton("➖ Вывести", callback_data="withdraw")))


@dp.message_handler(text='💳 Кошелек', state="*")
async def process_wallet(msg: types.Message, state: FSMContext):
    await process_state_wallet(msg)
    await state.finish()


'''#########investment########'''


@dp.message_handler(text='🖥 Инвестиции')
async def investment(message: types. Message):
    user = users.get_user(message.from_user.id)
    await message.answer_photo(caption='Открывайте свой вклад ниже, а после получайте прибыль с него и собирайте '
                                       'ее в данном разделе:\n\n'
                               f'📠 Процент от вклада: {investmen}%\n'
                               f'⏱ Время доходности: 24 часа\n'
                               f'📆 Срок вклада: Пожизненно\n\n'
                               f'💳 Ваш вклад: {round(user["investments"], 2)}₽\n'
                               f'💵 Накопление: {round(user["balance"], 2)}₽\n\n',
                               photo=types.InputFile(path.join('img', 'invest.jpeg')),
                               reply_markup=types.InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(
                                   "➕ Инвестировать", callback_data="invest"),
                                   InlineKeyboardButton("➖ Собрать", callback_data="collect")))


@dp.callback_query_handler(text="invest")
async def invest(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    await call.message.answer('Введите сумму которую хотите инвестировать:', reply_markup=types.ReplyKeyboardMarkup(
        resize_keyboard=True).add('назад'))
    await storege.set_state(chat=call.from_user.id, state='invest_amount')


@dp.message_handler(state='invest_amount')
async def invest_amount(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text.lower() == 'назад':
        await message.answer('© Главное меню.', reply_markup=user_menu)
        await state.finish()
        return
    try:
        amount = float(message.text)
        user = users.get_user(user_id)
        if float(user['balance']) < amount:
            raise ValueError
        users.change_investments(user_id, user['investments'] + amount)
        users.change_balance(user_id, user['balance'] - amount)
        await message.answer(f'Вы успешно инвестировали сумму {amount}')
        await message.answer('© Главное меню.', reply_markup=user_menu)
        await state.finish()
    except ValueError:
        await message.answer("На вашем счету недостаточно средств.\nПожалуйста, введите корректную сумму или нажмите"
                             "кнопку Назад")


@dp.callback_query_handler(text='collect')
async def collect(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    await call.message.answer('Введите сумму для вывода  средств:', reply_markup=types.ReplyKeyboardMarkup(
        resize_keyboard=True).add('назад'))
    await storege.set_state(chat=call.from_user.id, state='collect_amount')


@dp.message_handler(state='collect_amount')
async def collect_amount(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text.lower() == 'назад':
        await message.answer('© Главное меню.', reply_markup=user_menu)
        await state.finish()
        return
    try:
        amount = float(message.text)
        user = users.get_user(user_id)
        if float(user['investments']) < amount:
            raise ValueError
        users.change_investments(user_id, user['investments'] - amount)
        users.change_balance(user_id, user['balance'] + amount)
        await message.answer(f'Вы успешно вывели сумму {amount}')
        await message.answer('© Главное меню.', reply_markup=user_menu)
        await state.finish()
    except ValueError:
        await message.answer("На вашем счету недостаточно средств.\nПожалуйста, введите корректную сумму или нажмите"
                             "кнопку Назад")


@dp.message_handler(text='🖥 Инвестиции', state="*")
async def investments(msg: types.Message, state: FSMContext):
    await investmen(msg)
    await state.finish()








    # await message.answer(
    #     f"&#9899; Для начала работы с ботом, пройдите небольшую проверку, просто вступите в чат и канал ниже и нажмите "
    #     f"кнопку продолжить. <br><br> &#169; Нажмите на «Подписаться 1 и 2»", parse_mode='html')
    #
    # await asyncio.sleep(3)
    # await message.answer('⤵ Подпишитесь на чат/канал ⤵', reply_markup=user_key_board.main_menu_1)









# @dp.callback_query_handler(lambda x: x.data == 'Подписатся на канал')
# async def subscribe_to_channel(callback_query: CallbackQuery):
#     await callback_query.answer(text='Вы подписались на канал')
#
# @dp.callback_query_handler(lambda x: x.data == 'Подписатся на чат')
# async def subscribe_to_chat(callback_query: CallbackQuery):
#     await callback_query.answer(text='Вы подписались на чат')
#
# @dp.callback_query_handler(lambda x: x.data == 'Продолжить')
# async def continue_handler(callback_query: CallbackQuery):
#     await callback_query.answer(text='Вы продолжили')
#
#
#
#
# @dp.message_handler(text="🖥 Инвестиции")
# async def investments(message: types.Message):
#     await message.answer(text='Вы выбрали Инвестиции', reply_markup=user_key_board.main)
#
#
# @dp.message_handler(text="💳 Кошелёк"))
# async def balance(message: types.Message):
#     await message.answer(text='Вы выбрали Кошелёк', reply_markup=user_key_board.main)
#
#
# @dp.message_handler(text='📞 Контакты')
# async def contacts(message: Message):
#     await message.answer(text='Вы выбрали Контакты', reply_markup=user_key_board.main)
#
# @dp.message_handler(text="👥 Партнертньорам"))
# async def balfdsnce(message: types.Message):
#     await message.answer(text='Вы выбрали Партнерам', reply_markup=user_key_board.main)
#
#
# @dp.message_handler(text="🖨 Калькулятор"))
# async def profiler(message: types.Message, state: FSMContext):
#     await message.answer(text='Вы выбрали Калькулятор', reply_markup=user_key_board.main)
#
#
# @dp.message_handler(text="🗒 Обучение"))
# async def profile(message: types.Message):
#     await message.answer(text='Вы выбрали Обучение', reply_markup=user_key_board.main)
#
#
