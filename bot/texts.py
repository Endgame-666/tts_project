# Здесь находятся все возможные сообщения бота

def welcome_message(message):
    return (
        f"🎉 {message.from_user.full_name}, добро пожаловать! 🎭\n"
        f"С помощью этого бота ты можешь превратить любой текст в аудио 🎙️, "
        f"озвученное героями из фильмов 🎬, игр 🎮 и мультиков 🌟.\n"
        f"<b>Выбери голос или положись на случайный и вперёд!</b> 🚀"
    )


buttons = {
    "new_message": "🆕 Новый голос",
    "favorite_messages": "⭐️ Избранные сообщения",
    "random_voice": "🎲 Случайный голос",
}

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

start_working_text = "⏳ Начинаю обработку..."
didnt_choose_text = "🔍 Вы пока не сделали выбор. Нажмите кнопку ниже! 👇"

add_to_favorite_text = "⭐️ Добавить в избранное"
limit_favorite_text = "⛔️ Лимит избранного превышен!"
already_in_favorite_text = "🔁 Сообщение уже в избранном!"
favorite_msg_done_text = "✅ Сообщение добавлено в избранное!"
del_from_favorites_text = "❌ Удалить из избранного"
favorite_list_text = "🔊 Ваши избранные сообщения:"
no_favorite_list_text = "🎵 У вас пока нет избранных сообщений."
favorite_list_end_text = "✅ Список завершен"
deleted_from_favorite_text = "✅ Удалено из избранного"

