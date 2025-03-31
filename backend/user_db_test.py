import pytest
import pytest_asyncio
from pathlib import Path
import sqlite3
import json
from user_db import DatabaseManager  # замените your_module на имя вашего модуля
import aiosqlite


@pytest_asyncio.fixture
async def db_manager(tmp_path):
    db_path = tmp_path / "test.db"
    manager = DatabaseManager(str(db_path))
    yield manager




@pytest.mark.asyncio
async def test_create_tables(db_manager):
    """Проверяет корректное создание таблиц в базе данных при инициализации."""
    async with aiosqlite.connect(db_manager.db_name) as db:
        cursor = await db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        )
        result = await cursor.fetchone()
        assert result is not None
        assert result[0] == "users"


@pytest.mark.asyncio
async def test_add_user(db_manager):
    """Тестирует добавление пользователей: успешное создание и обработку дубликатов."""
    result = await db_manager.add_user(1, "TestUser")
    assert result is True

    result = await db_manager.add_user(1, "TestUser")
    assert result is False


@pytest.mark.asyncio
async def test_get_user(db_manager):
    """Проверяет получение данных пользователя для существующих и несуществующих записей."""
    user = await db_manager.get_user(1)
    assert user is None

    await db_manager.add_user(1, "TestUser")
    user = await db_manager.get_user(1)

    assert user["user_id"] == 1
    assert user["user_name"] == "TestUser"
    assert user["favourite_messages"] == []


@pytest.mark.asyncio
async def test_update_favourite_messages(db_manager):
    """Тестирует добавление сообщений в избранное и предотвращение дублирования."""
    user_id = 1
    test_message = "test_message.txt"

    await db_manager.add_user(user_id, "TestUser")

    await db_manager.update_favourite_messages(user_id, test_message)
    user = await db_manager.get_user(user_id)
    assert test_message in user["favourite_messages"]

    await db_manager.update_favourite_messages(user_id, test_message)
    user = await db_manager.get_user(user_id)
    assert len(user["favourite_messages"]) == 1


@pytest.mark.asyncio
async def test_remove_from_favourites(db_manager):
    """Проверяет удаление сообщений из избранного и обработку несуществующих записей."""
    user_id = 1
    test_message = "test_message.txt"

    await db_manager.add_user(user_id, "TestUser")
    await db_manager.update_favourite_messages(user_id, test_message)

    await db_manager.remove_from_favourites(user_id, test_message)
    user = await db_manager.get_user(user_id)
    assert test_message not in user["favourite_messages"]

    await db_manager.remove_from_favourites(user_id, "non_existent.txt")
    user = await db_manager.get_user(user_id)
    assert len(user["favourite_messages"]) == 0


@pytest.mark.asyncio
async def test_favourites_json_serialization(db_manager):
    """Проверяет корректность JSON-сериализации/десериализации избранных сообщений."""
    user_id = 1
    test_messages = ["msg1.txt", "msg2.txt"]

    await db_manager.add_user(user_id, "TestUser")
    async with aiosqlite.connect(db_manager.db_name) as db:
        await db.execute(
            "UPDATE users SET favourite_messages = ? WHERE user_id = ?",
            (json.dumps(test_messages), user_id)
        )
        await db.commit()

    user = await db_manager.get_user(user_id)
    assert user["favourite_messages"] == test_messages


@pytest.mark.asyncio
async def test_initial_favourites_empty(db_manager):
    """Проверяет, что новый пользователь имеет пустой список избранных сообщений."""
    await db_manager.add_user(1, "TestUser")
    user = await db_manager.get_user(1)
    assert user["favourite_messages"] == []


@pytest.mark.asyncio
async def test_user_name_update(db_manager):
    """Проверяет, что имя пользователя не обновляется при добавлении существующего ID."""
    await db_manager.add_user(1, "OldName")
    user = await db_manager.get_user(1)
    assert user["user_name"] == "OldName"

    await db_manager.add_user(1, "NewName")
    user = await db_manager.get_user(1)
    assert user["user_name"] == "OldName"


@pytest.mark.asyncio
async def test_multiple_favourites(db_manager):
    """Тестирует обработку нескольких избранных сообщений и проверку через множество."""
    user_id = 1
    messages = ["msg1.txt", "msg2.txt", "msg3.txt"]

    await db_manager.add_user(user_id, "TestUser")
    for msg in messages:
        await db_manager.update_favourite_messages(user_id, msg)

    user = await db_manager.get_user(user_id)
    assert len(user["favourite_messages"]) == 3
    assert set(user["favourite_messages"]) == set(messages)


@pytest.mark.asyncio
async def test_remove_from_empty_favourites(db_manager):
    """Проверяет корректную обработку удаления из пустого списка избранного."""
    user_id = 1
    await db_manager.add_user(user_id, "TestUser")

    await db_manager.remove_from_favourites(user_id, "any.txt")
    user = await db_manager.get_user(user_id)
    assert user["favourite_messages"] == []


@pytest.mark.asyncio
async def test_get_nonexistent_user(db_manager):
    """Проверяет обработку запроса несуществующего пользователя."""
    user = await db_manager.get_user(999)
    assert user is None


@pytest.mark.asyncio
async def test_sql_injection_safety(db_manager):
    """Тестирует защиту от SQL-инъекций и сохранность данных."""
    malicious_input = "test'; DROP TABLE users;--"

    await db_manager.add_user(1, malicious_input)
    user = await db_manager.get_user(1)
    assert user["user_name"] == malicious_input

    await db_manager.update_favourite_messages(1, malicious_input)
    user = await db_manager.get_user(1)
    assert malicious_input in user["favourite_messages"]

    async with aiosqlite.connect(db_manager.db_name) as db:
        cursor = await db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = await cursor.fetchall()
        assert ("users",) in tables