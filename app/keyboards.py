from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.logic import *

start_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='/flag')]],
    resize_keyboard=True,
)

kb_continents = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Европа', callback_data='continent:Европа')],
              [InlineKeyboardButton(text='Азия', callback_data='continent:Азия')],
              [InlineKeyboardButton(text='Южная Америка', callback_data='continent:ЮАмерика')],
              [InlineKeyboardButton(text='Северная Америка', callback_data='continent:САмерика')],
              [InlineKeyboardButton(text='Африка', callback_data='continent:Африка')],
              [InlineKeyboardButton(text='Океания', callback_data='continent:Океания')],
                [InlineKeyboardButton(text='Весь мир', callback_data='continent:Мир')]
              ]
)


def create_question(variants):
    keyboard = InlineKeyboardBuilder()

    for iso, country in variants:
        keyboard.add(
            InlineKeyboardButton(
                text=country,
                callback_data=f'answer_{iso}'))
    return keyboard.adjust(1).as_markup()
