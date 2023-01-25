from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_main_menu_kb():
    signal_button = InlineKeyboardButton(text='Сигнал', callback_data='signal')
    edit_button = InlineKeyboardButton(text='Редактирование', callback_data='edit')
    keyboard = InlineKeyboardMarkup(row_width=1).add(signal_button, edit_button)
    return keyboard


def home_kb():
    home_button = InlineKeyboardButton(text='🏠 Домой', callback_data='home')
    keyboard = InlineKeyboardMarkup(row_width=1).add(home_button)
    return keyboard


def signal_kb():
    signal_button = InlineKeyboardButton(text='Сигнал', callback_data='signal')
    home_button = InlineKeyboardButton(text='🏠 Домой', callback_data='home')
    keyboard = InlineKeyboardMarkup(row_width=1).add(signal_button, home_button)
    return keyboard
