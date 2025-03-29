import asyncio
import logging
import sys
import hashlib
import json

# aiogram
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.types import FSInputFile

# files
from bot.loading_messages import LoadingMessageManager
from bot.keyboards.main_keyboard import get_main_keyboard
from bot.settings import BOT_TOKEN
from bot.filters import *
from TTS.tts import get_voice
#rom database.database import *


dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = get_main_keyboard()
    await message.answer(welcome_message(message), reply_markup=keyboard)


@router.message(lambda message: message.web_app_data)
async def new_message_request(message: Message, state: FSMContext):
    web_data = message.web_app_data.data if message.web_app_data else None
    if web_data:
        try:
            data = json.loads(web_data)
            character_id = data.get('characterId', 0)

            await state.update_data(character_id=character_id)
            await state.set_state(MessageStates.waiting_for_message_request)

            CHARACTER_NAMES = {
                1: "Пудж 🔪⛓️💀",
                2: "Шрек 💚🤬",
                3: "Диппер 🧢🔦",
                4: "Мейбл ✨🦄",
                5: "Апвоут 💬❔",
                6: "Дональд Дак 🦆🌊😠",
                7: "Крош ⚡🐇",
                8: "Геральт ⚔️🐺",
                9: "Ургант 📺🎥",
                0: "🚫❓"
            }

            response = (
                f"🎉 Отличный выбор! 🎭\n"
                f"🎯 Ваш персонаж: <b>{CHARACTER_NAMES.get(character_id, 'неизвестный персонаж')}</b>\n"
                f"Теперь можно начинать озвучку! 🎙️\n"
                f"Напишите сообщение, которое хотите озвучить✍️"
            )

        except json.JSONDecodeError:
            response = "⚠️ Ошибка обработки выбора. Попробуйте еще раз!"
    else:
        response = "🔍 Вы пока не сделали выбор. Нажмите кнопку ниже! 👇"
    await message.answer(response)

def generate_safe_id(input_string: str) -> str:
    return hashlib.md5(input_string.encode()).hexdigest()

@router.message(StateFilter(MessageStates.waiting_for_message_request))
async def process_message_request(message: Message, state: FSMContext):
    loading_manager = LoadingMessageManager()
    loading_message = await message.answer("⏳ Начинаю обработку...")
    await loading_manager.start(loading_message)

    data = await state.get_data()
    character_id = data.get("character_id", 0)

    try:
        user_id = message.from_user.id
        message_text = message.text

        audio = get_voice(character_id, message_text)[2]
        audio_path = fr"{audio}"
        voice_file = FSInputFile(audio_path)

        message_id = generate_safe_id(audio_path)

        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text="Добавить в избранное",
                callback_data=MessageCallback(action="add", message_id=message_id).pack()
            )
        )

        await asyncio.sleep(3)
        await loading_manager.stop()
        await message.answer_voice(voice=voice_file, reply_markup=builder.as_markup())
        await state.set_state(MessageStates.waiting_for_message_request)

    except Exception as e:
        logging.error(f"Error in process_message_request: {e}")
        await state.clear()


@router.callback_query(MessageCallback.filter())
async def add_to_favorites(callback: CallbackQuery, callback_data: MessageCallback):
    if callback_data.action == "add":
        user_id = callback.from_user.id
        message_id = callback_data.message_id

        if user_id not in data:
            data[user_id] = []

        if message_id not in data[user_id]:
            data[user_id].append(message_id)
            await callback.answer("Добавлено в избранное!")
        else:
            await callback.answer("Уже в избранном!")


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
