import logging
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
import asyncio
BOT_TOKEN = "7751132273:AAGT6I6vOdqwDEZ-XL9yAT1VT-W5B8agsiU"

# Включаем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

from aiogram import types

@dp.update()
async def log_all_updates(update: types.Update):
    print(f"📩 Пришёл апдейт: {update}")

from aiogram.types import Message




@dp.message(F.text == '/start')  # или @dp.message(Command('start'))
async def start(message: types.Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="Открыть веб страницу",
                web_app=WebAppInfo(url="https://endgame-666.github.io/web_app_test/")
            )]
        ],
        resize_keyboard=True
    )
    await message.answer("Добро пожаловать!", reply_markup=markup)
#
# @router.message(Command("open"))
# async def open_webapp(message: types.Message):
#     markup = ReplyKeyboardMarkup(inline_keyboard=[
#         [KeyboardButton(
#             text="Выбрать котика 🐱",
#             web_app=WebAppInfo(url="https://cool-wasps-turn.loca.lt")
#         )]
#     ])
#     await message.answer("Открыть выбор котиков:", reply_markup=markup)

import json

@dp.message(lambda message: message.web_app_data)
async def web_app2(message: types.Message):
    logging.info(f"💬 Пришли данные: {message.web_app_data}")
    if message.web_app_data:
        await message.answer(f"Данные получены: {message.web_app_data.data}")
    else:
        await message.answer("😿 Данные не пришли!")


# @dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
# async def web_app_handler(message: Message):
#     data = message.web_app_data.data
#     await message.answer(f"✅ Бот получил данные: {data}")
#     print(f"📩 Данные от WebApp: {data}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())