import asyncio
import logging
import sys

# aiogram
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command, StateFilter
from aiogram.types import FSInputFile

# files
from bot.loading_messages import LoadingMessageManager
from bot.keyboards.main_keyboard import get_main_keyboard
from bot.settings import BOT_TOKEN
from bot.filters import *
from tts import split_text, get_voice

dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = get_main_keyboard()
    await message.answer(welcome_message(message), reply_markup=keyboard)


@router.message(lambda msg: msg.text == buttons["new_message"])
async def new_message_request(message: Message, state: FSMContext):
    await message.answer(
        new_message_welcome_text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Отмена")]],
            resize_keyboard=True
        )
    )
    await state.set_state(MessageStates.waiting_for_message_request)


@router.message(StateFilter(MessageStates.waiting_for_message_request))
async def process_message_request(message: Message, state: FSMContext):
    if message.text == "Отмена":
        await message.answer(
            "Конвертация сообщения в голос отменена",
            reply_markup=get_main_keyboard()
        )
        await state.clear()
        await message.answer("Выберите действие:", reply_markup=get_main_keyboard())
        return

    loading_message = await message.answer("🔍 Начинаю конвертацию голоса...")
    loading_manager = LoadingMessageManager(loading_message)

    try:
        await loading_manager.start()

        user_id = message.from_user.id
        message_text = message.text
        voice_name, text = split_text(message_text)

        audio_path = fr"{get_voice(voice_name, text)[2]}"
        voice_file = FSInputFile(audio_path)

        await asyncio.sleep(3)
        await loading_manager.stop()

        await message.answer_voice(voice=voice_file)

        await message.answer("Выберите действие:", reply_markup=get_main_keyboard())
        await state.clear()

    except Exception as e:
        await state.clear()




async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
