# Здесь находятся все возможные сообщения бота

def welcome_message(message):
    return (
        f"🎉 {message.from_user.full_name}, добро пожаловать! 🎭\n"
        f"С помощью этого бота ты можешь превратить любой текст в аудио 🎙️, "
        f"озвученное героями из фильмов 🎬, игр 🎮 и мультиков 🌟.\n"
        f"<b>Выбери голос и вперёд!</b> 🚀"
    )


buttons = {
    "new_message": "🆕 Новый голос",
    "favorite_messages": "⭐️ Избранные сообщения",
    "random_voice": "🎲 Случайный голос",
}

favourite_messages_response = "Избранные сообщения:"
message_history_response = "История ваших сообщений:"


