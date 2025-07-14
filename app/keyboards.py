from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

limit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Время", callback_data="time")],
    [InlineKeyboardButton(text="Кол-во сообщений", callback_data="count")]
])

period = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Годах", callback_data="years")],
    [InlineKeyboardButton(text="Месяцах", callback_data="months")],
    [InlineKeyboardButton(text="Днях", callback_data="days")]
])

yes_no = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="yes")],
    [InlineKeyboardButton(text="Нет", callback_data="no")]
])