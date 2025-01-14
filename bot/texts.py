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
preferences_response = "Настройки личных предпочтений:"

preferences = {
    "allergies": "Аллергия",
    "price_limit": "Ограничение цены",
    "disliked_products": "Нелюбимые продукты",
    "view_preferences": "Посмотреть мои предпочтения",
    "back": "Назад",
}