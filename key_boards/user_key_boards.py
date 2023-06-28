from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("/start"))


# main_buttons = [
#     [
#         KeyboardButton(text='🖥 Инвестиции', callback_data='investments'),
#         KeyboardButton(text='💳 Кошелёк', callback_data='currency'),
#         KeyboardButton(text='📞 Контакты', callback_data='contacts'),
#     ],
#     [
#         KeyboardButton(text='👥 Партнерам', callback_data='part'),
#         KeyboardButton(text='🖨 Калькулятор', callback_data='calc'),
#         KeyboardButton(text='🗒 Обучение', callback_data='gide'),
#     ]
# ]
# main = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=main_buttons)
user_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).row('🖥 Инвестиции', '👔 Партнерам')
user_menu.add('💳 Кошелек', '⌨ Калькулятор')
user_menu.add('📞 Контакты', '🗓 Обучения')

