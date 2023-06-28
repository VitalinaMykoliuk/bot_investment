from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


admin_action = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).row\
    ('⚙️ Регулировка баланса', '❌ Бан Юзера', '🗒 Статистика')