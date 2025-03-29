import random
import asyncio
from aiogram.types import Message

loading_messages = [
    "🔍 Ищу лучшие голоса...",
    "📝 Подбираю тоны...",
    "⚖️ Рассчитываю длину...",
    "📊 Анализирую отзывы...",
    "💡 Подбираю альтернативные варианты...",
    "⭐️ Выбираю лучшие предложения...",
    "🔄 Обрабатываю информацию...",
    "🎭 Загружаю характер персонажа...",
    "🔮 Синхронизирую с оригиналом...",
    "🎙️ Настраиваю тембр голоса...",
    "📚 Проверяю лор вселенной...",
    "🎨 Добавляю уникальные эффекты...",
    "🛠️ Оптимизирую аудиодорожку...",
    "🎮 Подключаю игровые модули...",
    "🎬 Анализирую кинопленку...",
    "🧪 Тестирую голосовые паттерны...",
    "🌐 Перевод в мультивселенную...",
    "🦸♂️ Загружаю суперспособности...",
    "🎵 Синтезирую вокальные треки...",
    "🤖 Калибрую нейросеть...",
    "📡 Связываюсь с голосовой базой...",
    "🎚️ Выравниваю громкость...",
    "👾 Имитирую цифровое сознание...",
    "🧙♂️ Призываю магию озвучки...",
    "🕹️ Активирую игровой режим...",
    "🎭 Примеряю голосовую маску...",
    "🔊 Тестирую акустику..."
]

def get_random_loading_message() -> str:
    return random.choice(loading_messages)


class LoadingMessageManager:
    def __init__(self):
        self.is_running = True
        self.task = None
        self.message = None
        self.last_content = None

    async def update_loading_message(self):
        """Обновляет сообщение с анимацией загрузки"""
        while self.is_running:
            try:
                loading_text = get_random_loading_message()
                unique_suffix = "".join(random.choices(".: ", k=2))
                loading_text = f"{loading_text}{unique_suffix}"

                if loading_text != self.last_content and self.message:
                    await self.message.edit_text(loading_text)
                    self.last_content = loading_text

            except Exception as e:
                if "message to edit not found" in str(e):
                    self.is_running = False
                print(f"Error updating loading message: {e}")

            await asyncio.sleep(0.7)

    async def start(self, initial_message: Message):
        """Инициализирует и запускает анимацию"""
        try:
            self.message = initial_message
            self.task = asyncio.create_task(self.update_loading_message())
        except Exception as e:
            print(f"Error starting loading message: {e}")

    async def stop(self):
        """Останавливает анимацию и удаляет сообщение"""
        self.is_running = False
        if self.task:
            try:
                self.task.cancel()
                await self.task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                print(f"Error stopping task: {e}")
        if self.message:
            try:
                await self.message.delete()
            except Exception as e:
                print(f"Error deleting message: {e}")
