from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.database import MongoDBManager  # Замените на ваш модуль БД


class VoiceMessageCallback(CallbackData, prefix="voice_msg"):
    action: str  # "add", "remove", "view"
    message_id: str


class FavoriteHandler:
    def __init__(self):
        mongo_url = "your_mongo_connection_string"
        self.db = MongoDBManager(
            mongo_url=mongo_url,
            db_name="voice_bot",
            collection_name="favorites"
        )

    async def toggle_favorite(self, user_id: int, message_id: str) -> bool:
        """Добавляет/удаляет сообщение из избранного"""
        user_favorites = await self.get_favorites(user_id)

        if message_id in user_favorites:
            await self.db.delete_one(
                {"user_id": user_id},
                {"$pull": {"favorites": message_id}}
            )
            return False
        else:
            await self.db.update_one(
                {"user_id": user_id},
                {"$addToSet": {"favorites": message_id}},
                upsert=True
            )
            return True

    async def get_favorites(self, user_id: int) -> list:
        """Возвращает список избранных сообщений пользователя"""
        result = await self.db.find_one({"user_id": user_id})
        return result.get("favorites", []) if result else []

    async def is_favorite(self, user_id: int, message_id: str) -> bool:
        """Проверяет, есть ли сообщение в избранном"""
        return message_id in await self.get_favorites(user_id)


# Инициализация хэндлера
favorite_handler = FavoriteHandler()


@router.callback_query(VoiceMessageCallback.filter())
async def handle_favorites(callback: CallbackQuery,
                           callback_data: VoiceMessageCallback):
    user_id = callback.from_user.id
    message_id = callback_data.message_id

    if callback_data.action == "add":
        # Добавление в избранное
        is_favorite = await favorite_handler.toggle_favorite(user_id, message_id)
        text = "✅ Добавлено в избранное!" if is_favorite else "❌ Удалено из избранного"
        await callback.answer(text)

    elif callback_data.action == "view":
        # Просмотр избранного
        favorites = await favorite_handler.get_favorites(user_id)
        if not favorites:
            await callback.answer("📭 Список избранного пуст")
            return

        # Отправка первого сообщения из списка
        first_message_id = favorites[0]
        await send_favorite_message(callback.message, first_message_id)

    # Обновляем клавиатуру
    await update_message_keyboard(callback.message, message_id, user_id)


async def send_favorite_message(message: Message, message_id: str):
    # Ваша логика получения и отправки сообщения по ID
    # Например:
    voice_data = await get_voice_message_from_db(message_id)
    await message.answer_voice(voice_data['file_id'])


async def update_message_keyboard(message: Message, message_id: str, user_id: int):
    is_favorite = await favorite_handler.is_favorite(user_id, message_id)
    button_text = "❌ Удалить из избранного" if is_favorite else "⭐️ В избранное"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=button_text,
            callback_data=VoiceMessageCallback(
                action="add",
                message_id=message_id
            ).pack()
        )],
        [InlineKeyboardButton(
            text="📂 Показать избранное",
            callback_data=VoiceMessageCallback(
                action="view",
                message_id="0"
            ).pack()
        )]
    ])

    await message.edit_reply_markup(reply_markup=keyboard)