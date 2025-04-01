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
-- user_feedback_db
CREATE TABLE IF NOT EXISTS feedback_voices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    voice_name TEXT NOT NULL
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

## ❗️ Важные ссылки

🔹 **Сервис RVC для обучения моделей**  
_Этот репозиторий содержит инструменты для создания и дообучения голосовых моделей с использованием Retrieval-based Voice Conversion (RVC)._  
[GitHub: RVC-Project](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)

🔹 **Web-интерфейс RVC-WebUI для синтеза речи готовых моделей**  
_Позволяет загружать уже обученные модели и синтезировать голос, используя браузерный интерфейс._  
[GitHub: RVC-WebUI](https://github.com/litagin02/rvc-tts-webui)

🔹 **Telegram-Mini-App для проекта на базе GitHub Pages**  
_Мини-приложение для Telegram, интегрированное с нашим сервисом TTS, разработанное на базе GitHub.io._  
[GitHub: TTS Mini App](https://github.com/Endgame-666/tts_project_mini_app)

## 🎙️ Доступные голосовые модели

- **Pudge** 🔪⛓️💀  
- **Шрек** 💚🤬  
- **Диппер** 🧢🔦  
- **Мейбл** ✨🦄  
- **Апвоут** 💬❔  
- **Дональд Дак** 🦆🌊😠  
- **Крош** ⚡🐇  
- **Геральт** ⚔️🐺  
- **Ургант** 📺🎥  
- **В.В.Путин** 👑🐻  
- **Pangolier** ⚔️🛡️🌪️  
- **Crystal Maiden** ❄️🌀🔮  
- **Mr.Beast** 😎💥🚀  
- **В.В.Жириновский** 🗣️🔥  
- **Копатыч** 🐻🍯🌿  
- **Лунтик** 🌙✨🐝  
- **Нолик** 🔧⚡🔩  
- **Эрен Йегер** ⚔️🔥💢  
- **Shadow Fiend** 💀🔥🌑  
- **Джинкс** 💣😈🎭  

## 📞 Контакты

По всем вопросам: [@endgame_666](https://t.me/endgame_666)