from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.logic import *

start_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='/flag')]],
    resize_keyboard=True,
)

def create_question(variants):
    keyboard = InlineKeyboardBuilder()

    for iso,country in variants:
        keyboard.add(
            InlineKeyboardButton(
                text=country,
                callback_data=f'answer_{iso}'))
    return keyboard.adjust(1).as_markup()
