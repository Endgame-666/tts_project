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
