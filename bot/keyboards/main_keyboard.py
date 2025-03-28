from aiogram.types import ReplyKeyboardMarkup, KeyboardButton # type: ignore
from aiogram.utils.keyboard import ReplyKeyboardBuilder # type: ignore
from bot.texts import *
from aiogram.types.web_app_info import WebAppInfo

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text=buttons["new_message"],
                   web_app=WebAppInfo(url="https://endgame-666.github.io/tts_project/"))
    builder.button(text=buttons["favorite_messages"])
    builder.button(text=buttons["message_history"])
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)