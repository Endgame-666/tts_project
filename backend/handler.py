from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
import asyncio
import logging
import json
from database.user_db import DatabaseManager

router = Router()

db_manager = DatabaseManager()


@router.message(Command("favorites"))
async def get_favorites(message: types.Message):
    """Получает список избранных сообщений пользователя."""
    user_id = message.from_user.id
    user_data = await db_manager.get_user(user_id)

    if not user_data or not user_data["favourite_messages"]:
        await message.answer("У вас пока нет избранных сообщений.")
        return

    text = "Ваши избранные сообщения:\n" + "\n".join(user_data["favourite_messages"])
    await message.answer(text)


@router.callback_query(lambda c: c.data.startswith("add_favorite"))
async def add_to_favorites(callback: types.CallbackQuery):
    """Добавляет сообщение в избранное пользователя, если лимит не превышен."""
    user_id = callback.from_user.id
    message_id = callback.data.split(":")[1]

    user_data = await db_manager.get_user(user_id)
    favourites = user_data["favourite_messages"] if user_data else []

    if len(favourites) >= 5:
        await callback.answer("Вы не можете добавить больше 5 избранных сообщений.")
        return

    if message_id in favourites:
        await callback.answer("Это сообщение уже в избранном!")
        return

    await db_manager.update_favourite_recipes(user_id, message_id)
    await callback.answer("Сообщение добавлено в избранное!")


@router.callback_query(lambda c: c.data.startswith("remove_favorite"))
async def remove_from_favorites(callback: types.CallbackQuery):
    """Удаляет сообщение из избранного."""
    user_id = callback.from_user.id
    message_id = callback.data.split(":")[1]

    user_data = await db_manager.get_user(user_id)
    favourites = user_data["favourite_messages"] if user_data else []

    if message_id not in favourites:
        await callback.answer("Этого сообщения нет в избранном.")
        return

    favourites.remove(message_id)
    await db_manager.update_favourite_recipes(user_id, json.dumps(favourites))
    await callback.answer("Сообщение удалено из избранного!")
