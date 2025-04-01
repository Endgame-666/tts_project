import pytest
import pytest_asyncio
import aiosqlite
from datetime import datetime
from backend.message_db import DatabaseMessageManager


@pytest_asyncio.fixture
async def db_manager(tmp_path):
    db_path = tmp_path / "test.db"
    manager = DatabaseMessageManager(str(db_path))
    return manager


@pytest.mark.asyncio
async def test_create_messages_table(db_manager):
    """Проверка создания таблицы messages"""
    async with aiosqlite.connect(db_manager.db_name) as db:
        cursor = await db.execute("PRAGMA table_info(messages)")
        columns = await cursor.fetchall()

        expected_columns = [
            ('file_path', 'TEXT', 0, None, 1),
            ('message_text', 'TEXT', 1, None, 0),
            ('hero_id', 'INT', 1, None, 0),
            ('created_at', 'TIMESTAMP', 0, None, 0)
        ]

        assert len(columns) == 4
        for col, expected in zip(columns, expected_columns):
            assert (col[2], col[3], col[5]) == (expected[1], expected[2], expected[4])


@pytest.mark.asyncio
async def test_save_new_message(db_manager):
    """Сохранение нового сообщения"""
    await db_manager.save_message("test.mp3", "Hello", 1)

    async with aiosqlite.connect(db_manager.db_name) as db:
        cursor = await db.execute("SELECT * FROM messages")
        result = await cursor.fetchone()
        assert result == ("test.mp3", "Hello", 1, result[3])


@pytest.mark.asyncio
async def test_update_existing_message(db_manager):
    """Обновление существующей записи"""
    await db_manager.save_message("test.mp3", "Hello", 1)
    await db_manager.save_message("test.mp3", "Updated", 2)

    message = await db_manager.get_message_text("test.mp3")
    assert message["text"] == "Updated"
    assert message["character"] == 2


@pytest.mark.asyncio
async def test_get_existing_message(db_manager):
    """Получение существующего сообщения"""
    await db_manager.save_message("test.mp3", "Test message", 5)
    result = await db_manager.get_message_text("test.mp3")

    assert result == {"text": "Test message", "character": 5}


@pytest.mark.asyncio
async def test_get_nonexistent_message(db_manager):
    """Попытка получить несуществующее сообщение"""
    result = await db_manager.get_message_text("nonexistent.mp3")
    assert result is None


@pytest.mark.asyncio
async def test_delete_existing_message(db_manager):
    """Удаление существующего сообщения"""
    await db_manager.save_message("test.mp3", "Hello", 1)
    result = await db_manager.delete_message("test.mp3")
    assert result is False


@pytest.mark.asyncio
async def test_delete_nonexistent_message(db_manager):
    """Попытка удалить несуществующее сообщение"""
    result = await db_manager.delete_message("nonexistent.mp3")
    assert result is False


@pytest.mark.asyncio
async def test_created_at_auto_populated(db_manager):
    """Проверка автоматического заполнения времени создания"""
    await db_manager.save_message("test.mp3", "Hello", 1)

    async with aiosqlite.connect(db_manager.db_name) as db:
        cursor = await db.execute("SELECT created_at FROM messages")
        result = await cursor.fetchone()
        created_at = datetime.fromisoformat(result[0])
        assert isinstance(created_at, datetime)


@pytest.mark.asyncio
async def test_save_message_sql_injection(db_manager):
    """Проверка защиты от SQL-инъекций"""
    malicious_path = "test'; DROP TABLE messages;--"
    await db_manager.save_message(malicious_path, "Hack", 1)

    result = await db_manager.get_message_text(malicious_path)
    assert result is not None

    async with aiosqlite.connect(db_manager.db_name) as db:
        cursor = await db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = await cursor.fetchall()
        assert ("messages",) in tables


@pytest.mark.asyncio
async def test_save_message_data_types(db_manager):
    """Проверка корректности типов данных"""
    await db_manager.save_message("test.mp3", 12345, "5")

    async with aiosqlite.connect(db_manager.db_name) as db:
        cursor = await db.execute("SELECT message_text, hero_id FROM messages")
        result = await cursor.fetchone()
        assert result == ("12345", 5)


@pytest.mark.asyncio
async def test_duplicate_file_path_constraint(db_manager):
    """Проверка уникальности file_path"""
    await db_manager.save_message("duplicate.mp3", "First", 1)
    await db_manager.save_message("duplicate.mp3", "Second", 2)

    async with aiosqlite.connect(db_manager.db_name) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM messages")
        count = await cursor.fetchone()
        assert count[0] == 1


@pytest.mark.asyncio
async def test_null_constraints(db_manager):
    """Проверка ограничений NOT NULL"""
    with pytest.raises(Exception):
        await db_manager.save_message("null_test.mp3", None, 1)

    with pytest.raises(Exception):
        await db_manager.save_message("null_test2.mp3", "Text", None)


@pytest.mark.asyncio
async def test_long_text_handling(db_manager):
    """Проверка обработки длинных текстов"""
    long_text = "A" * 10000
    await db_manager.save_message("long.mp3", long_text, 1)

    result = await db_manager.get_message_text("long.mp3")
    assert result["text"] == long_text


@pytest.mark.asyncio
async def test_special_characters(db_manager):
    """Проверка специальных символов в данных"""
    test_text = "漢字\n\t\\U0001f600 &%$#@!"
    await db_manager.save_message("special.mp3", test_text, 999)

    result = await db_manager.get_message_text("special.mp3")
    assert result["text"] == test_text


@pytest.mark.asyncio
async def test_created_at_not_updated_on_replace(db_manager):
    """Проверка что created_at не обновляется при замене записи"""
    await db_manager.save_message("replace.mp3", "First", 1)

    async with aiosqlite.connect(db_manager.db_name) as db:
        cursor = await db.execute("SELECT created_at FROM messages")
        first_time = await cursor.fetchone()

    await db_manager.save_message("replace.mp3", "Second", 2)

    async with aiosqlite.connect(db_manager.db_name) as db:
        cursor = await db.execute("SELECT created_at FROM messages")
        second_time = await cursor.fetchone()
        assert first_time[0] == second_time[0]


@pytest.mark.asyncio
async def test_multiple_hero_ids(db_manager):
    """Проверка хранения разных hero_id"""
    test_data = [
        ("msg1.mp3", "Text1", 1),
        ("msg2.mp3", "Text2", 2),
        ("msg3.mp3", "Text3", 3)
    ]

    for path, text, hero_id in test_data:
        await db_manager.save_message(path, text, hero_id)

    async with aiosqlite.connect(db_manager.db_name) as db:
        cursor = await db.execute("SELECT hero_id FROM messages")
        results = await cursor.fetchall()
        heroes = {row[0] for row in results}
        assert heroes == {1, 2, 3}
