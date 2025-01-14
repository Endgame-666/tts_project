from aiogram.types import ReplyKeyboardMarkup, KeyboardButton # type: ignore
from aiogram.utils.keyboard import ReplyKeyboardBuilder # type: ignore
from .. import texts

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text=texts.buttons["new_message"])
    builder.button(text=texts.buttons["favorite_messages"])
    builder.button(text=texts.buttons["message_history"])
    builder.button(text=texts.buttons["preferences"])
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)