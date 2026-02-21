from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def admin_kb():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Получить список результатов")]],
                               resize_keyboard=True,
                               one_time_keyboard=False,
                               is_persistent=True)
