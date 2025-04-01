# Telegram bot for text-to-speech with customizable voices (Telegram-бот для озвучивания текста с выбором голосов)

Проект представляет собой Telegram-бот, позволяющий пользователям озвучивать текстовые сообщения голосами различных персонажей из фильмов и игр, создавая эффект личного общения и добавляя элемент развлечения в общение. Пользователь может выбирать, чьим голосом будет зачитано сообщение, создавая уникальные аудиосообщения, которые имитируют известные голоса.

## 🚀 Возможности

- 🎭 конвертация текста в речь выбранным голосом
- 📝 Обработка выбранного голоса для синтеза речи
- 🧮 Добавления голоса в избранные  
- 👂 Прослушивание примеров голосов для точного выбора
- 💾 Сохранение любимых сообщений в избранном
- 🎰 Выбор голоса случайным образом

## 🏗 Структура проекта

```
tts_project/
├── TTS/
│   ├── models.py
│   └── tts.py
├── backend/
│   ├──  message_db.py
│   └──  user_db.py
├── bot/
│   ├── filters.py
│   ├── loading_messages.py
│   ├── main_keyboard.py
│   └── texts.py
├── frontend/
│   ├── audio/
│   ├── css/
│   ├── js/
│   ├── pictures/
│   └── index.html
├── tests/
│   ├── message_db_test.py
│   ├── test_bot.py
│   └── user_db_test.py
└── main.py
```
## 📊 Базы данных
```sql
-- user_db
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT,
    favourite_messages TEXT
);

-- message_db
CREATE TABLE IF NOT EXISTS messages (
    file_path TEXT PRIMARY KEY,
    message_text TEXT NOT NULL,
    hero_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
## 🗾 Архитектура сервиса и пользовательские сценарии
- https://miro.com/app/board/uXjVLGen_eE=/