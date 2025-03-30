import asyncio
import logging
import random
import sys
import hashlib
import json
import os

# aiogram
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.types import FSInputFile
from aiogram import F

# files
from bot.loading_messages import LoadingMessageManager
from bot.main_keyboard import get_main_keyboard
from bot.settings import BOT_TOKEN
from bot.filters import *
from TTS.tts import get_voice
from backend.database.user_db import DatabaseManager
from bot.texts import *

db_manager = DatabaseManager()
dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = get_main_keyboard()
    await message.answer(welcome_message(message), reply_markup=keyboard)


@router.message(F.web_app_data.is_not(None))
async def new_message_request(message: Message, state: FSMContext):
    """Получение данных с mini app о выбранном голосе"""
    web_data = message.web_app_data.data if message.web_app_data else None
    if web_data:
        try:
            data = json.loads(web_data)
            character_id = data.get('characterId', 0)

            await state.update_data(character_id=character_id)
            await state.set_state(MessageStates.waiting_for_message_request)

            response = (
                f"🎉 Отличный выбор! 🎭\n"
                f"🎯 Ваш персонаж: <b>{CHARACTER_NAMES.get(character_id, 'неизвестный персонаж')}</b>\n"
                f"Теперь можно начинать озвучку! 🎙️\n"
                f"Напишите сообщение, которое хотите озвучить✍️"
            )

        except json.JSONDecodeError:
            response = "⚠️ Ошибка обработки выбора. Попробуйте еще раз!"
    else:
        response = didnt_choose_text
    await message.answer(response)



def generate_safe_id(input_string: str) -> str:
    return hashlib.md5(input_string.encode()).hexdigest()

@router.message(F.text == buttons["favorite_messages"] )
async def get_favorites(message: Message):
    """Показать избранные сообщения"""
    user_id = message.from_user.id
    user_data = await db_manager.get_user(user_id)

    if not user_data or not user_data["favourite_messages"]:
        await message.answer(no_favorite_list_text)
        return

    await message.answer(favorite_list_text)
    favourites = user_data["favourite_messages"]
    for audio_path in favourites:
        try:
            folder_name = os.path.basename(os.path.dirname(audio_path))
            file = FSInputFile(audio_path)

            builder = InlineKeyboardBuilder()
            builder.row(
                InlineKeyboardButton(
                    text=del_from_favorites_text,
                    callback_data=MessageCallback(
                        action="del",
                        message_file=folder_name
                    ).pack()
                )
            )

            await message.answer_audio(
                audio=file,
                reply_markup=builder.as_markup()
            )

        except Exception as e:
            print(f"Ошибка: {e}")
            await message.answer("❌ Ошибка загрузки аудио")

    await message.answer(favorite_list_end_text)


@router.message(F.text == buttons["random_voice"])
async def process_message_request_random(message: Message, state: FSMContext):
    """Выбрать голос случайным образом"""
    character_id = random.randint(1, 12)
    await state.update_data(character_id=character_id)
    await state.set_state(MessageStates.waiting_for_message_request)
    response = (
        f"🎰 Рулетка голосов! 🎭\n"
        f"🎉 Вам попался: <b>{CHARACTER_NAMES.get(character_id, 'уникальный голос')}</b>\n"
        f"🔊 Погнали озвучивать! Пишите текст для превращения 🎙️➡️🔮"
    )
    await message.answer(response)


@router.message(StateFilter(MessageStates.waiting_for_message_request))
async def process_message_request(message: Message, state: FSMContext):
    """Главная функция, возвращает голосовое сообщение выбранным голосом"""
    loading_manager = LoadingMessageManager()
    loading_message = await message.answer(start_working_text)
    await loading_manager.start(loading_message)

    data = await state.get_data()
    character_id = data.get("character_id", 0)

    try:
        user_id = message.from_user.id
        message_text = message.text

        audio = get_voice(character_id, message_text)[2]
        audio_path = fr"{audio}"
        voice_file = FSInputFile(audio_path)

        folder_name = os.path.basename(os.path.dirname(audio_path))
        message_id = generate_safe_id(audio_path)
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text=add_to_favorite_text,
                callback_data=MessageCallback(action="add", message_file=folder_name).pack()
            )
        )

        await asyncio.sleep(3)
        await loading_manager.stop()
        await message.answer_voice(voice=voice_file, reply_markup=builder.as_markup())

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await state.clear()



@router.callback_query(MessageCallback.filter(F.action == "add"))
async def add_to_favorites(callback: CallbackQuery):
    """Добавляет в избранное сообщение"""
    if callback.data.split(":")[1] == "add":
        user_id = callback.from_user.id
        try:
            message_file = callback.data.split(":")[2]
        except IndexError:
            await callback.answer("Ошибка в данных сообщения.")
            return

        file = fr"C:\Users\Вадим\AppData\Local\Temp\gradio\{message_file}\audio.wav"

        user_data = await db_manager.get_user(user_id)
        if not user_data:
            user_name = callback.from_user.full_name or "Unknown"
            added = await db_manager.add_user(user_id, user_name)
            if not added:
                await callback.answer("Ошибка при создании пользователя.")
                return
            user_data = await db_manager.get_user(user_id)

        favourites = user_data["favourite_messages"]

        if len(favourites) >= 5 and file not in favourites:
            await callback.answer(limit_favorite_text)
            return

        if file in favourites:
            await callback.answer(already_in_favorite_text)
            return

        try:
            await db_manager.update_favourite_messages(user_id, file)
            await callback.answer(favorite_msg_done_text)
        except Exception as e:
            print(f"Ошибка: {e}")
            await callback.answer("Произошла ошибка.")




@router.callback_query(MessageCallback.filter(F.action == "del"))
async def remove_from_favorites(
        callback: CallbackQuery,
        callback_data: MessageCallback
):
    """Удаляет сообщение из избранного"""
    user_id = callback.from_user.id
    user_data = await db_manager.get_user(user_id)
    file_id = callback_data.message_file
    target_path = fr"C:\Users\Вадим\AppData\Local\Temp\gradio\{file_id}\audio.wav"

    await db_manager.remove_from_favourites(user_id, target_path)
    await callback.answer(deleted_from_favorite_text)
    await callback.message.delete()

@router.message()
async def handle_unknown(message: Message):
    """Когда еще ничего не выбрали"""
    await message.answer(didnt_choose_text)

async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
