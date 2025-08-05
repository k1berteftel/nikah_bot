from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_extend_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Продлить подписку', callback_data='sub_extend')]]
    )