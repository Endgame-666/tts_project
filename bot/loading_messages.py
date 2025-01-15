import random
import asyncio
from aiogram.types import Message

loading_messages = [
    "🔍 Ищу лучшие рецепты...",
    "📝 Подбираю ингредиенты...",
    "🛒 Ищу самые выгодные цены на продукты...",
    "⚖️ Рассчитываю пропорции...",
    "🧮 Оптимизирую список покупок...",
    "📊 Анализирую отзывы...",
    "🏪 Проверяю наличие продуктов...",
    "💡 Подбираю альтернативные варианты...",
    "⭐️ Выбираю лучшие предложения...",
    "🔄 Обрабатываю информацию...",
    "🏃‍♂️‍➡️ Бегаю по магазинам...",
    "🧏 Сигма сигма бой",
    "🌱 Сажаю ростки...",
    "☕ Несу кофе Феде...",
]

def get_random_loading_message() -> str:
    return random.choice(loading_messages)

class LoadingMessageManager:
    def __init__(self, message: Message):
        self.message = message
        self.is_running = True
        self.task = None
        self.current_operation = "🔍 Начинаю конвертацию голоса..."

    async def update_loading_message(self):
        while self.is_running:
            try:
                loading_text = get_random_loading_message()
                if not loading_text.endswith('...'):
                    loading_text += '...'
                await self.message.edit_text(loading_text)
            except Exception as e:
                print(f"Error updating loading message: {e}")
            finally:
                if self.is_running:
                    await asyncio.sleep(1)

    async def start(self):
        self.task = asyncio.create_task(self.update_loading_message())
        return self.task

    async def stop(self):
        self.is_running = False
        if self.task and not self.task.done():
            try:
                self.task.cancel()
                await self.task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                print(f"Error stopping loading message task: {e}")