def welcome_message(message):
    return (
        f"{message.from_user.full_name}, добро пожаловать! Выберите действие:"
    )


buttons = {
    "new_message": "🆕 Новое сообщение",
    "favorite_messages": "⭐️ Избранные сообщения",
    "message_history": "📜 История сообщений",
    "preferences": "⚙️ Личные предпочтения",
}

new_message_response = "Введите название блюда и количество порций"
favourite_messages_response = "Избранные сообщения:"
message_history_response = "История ваших сообщений:"

new_message_welcome_text = (
    "Пожалуйста, напишите голос, которым хотите зачитать сообщение\n"
    "в формате &ltголос&gt:&ltваше сообщение&gt\n"
    "Например: Гарри Поттер: Волендеморт лох!\n"
    "\n"
    "Доступные голоса:\n"
    "Квопа\n"
    "Путин\n"
    "Джарвис\n"
    "Валакас\n"
)
