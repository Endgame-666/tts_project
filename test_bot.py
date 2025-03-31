import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.types import Message, WebAppInfo, WebAppData, CallbackQuery, User, Chat, Voice, Audio
from aiogram.fsm.context import FSMContext
import os
from main import (
    dp,
    cmd_start,
    new_message_request,
    handle_specific_types,
    get_favorites,
    process_message_request_random,
    process_message_request,
    add_to_favorites,
    remove_from_favorites,
    handle_unknown,
    CHARACTER_NAMES,
    buttons,
    MessageStates,
    MessageCallback,
    validate_text_length,
    generate_safe_id
)
from bot.texts import (
    welcome_message,
    didnt_choose_text,
    specific_type_text,
    no_favorite_list_text,
    favorite_list_text,
    favorite_list_end_text,
    add_to_favorite_text,
    del_from_favorites_text,
    limit_favorite_text,
    already_in_favorite_text,
    favorite_msg_done_text,
    deleted_from_favorite_text
)


@pytest.fixture
def mock_message():
    message = MagicMock(spec=Message)
    user = MagicMock(spec=User)
    user.id = 123
    user.full_name = "Test User"
    message.from_user = user
    message.answer = AsyncMock()
    return message


@pytest.fixture
def mock_callback():
    callback = MagicMock(spec=CallbackQuery)
    user = MagicMock(spec=User)
    user.id = 123
    callback.from_user = user
    callback.message = MagicMock()
    callback.answer = AsyncMock()
    return callback




@pytest.mark.asyncio
async def test_new_message_request_valid_data(mock_message):
    mock_message.web_app_data = WebAppData(
        data='{"characterId": 1}',
        button_text="Choose Character"
    )
    state = MagicMock(spec=FSMContext)
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()

    await new_message_request(mock_message, state)

    mock_message.answer.assert_called_once()
    state.update_data.assert_called_once_with(character_id=1)
    state.set_state.assert_called_once_with(MessageStates.waiting_for_message_request)


@pytest.mark.asyncio
async def test_handle_specific_types(mock_message):
    mock_message.content_type = "photo"
    await handle_specific_types(mock_message)
    mock_message.answer.assert_called_once_with("🤷‍♂️ Непонятный формат. Отправьте, пожалуйста, текст")


@pytest.mark.asyncio
async def test_get_favorites_no_data(mock_message):
    with patch("main.db_manager.get_user", AsyncMock(return_value=None)):
        await get_favorites(mock_message)
        mock_message.answer.assert_called_with(no_favorite_list_text)


@pytest.mark.asyncio
@patch("main.os.path.basename")
@patch("main.FSInputFile")
async def test_get_favorites_with_data(mock_fsinput, mock_basename, mock_message):
    test_data = {"favourite_messages": ["/path/to/audio1.wav"]}

    with patch("main.db_manager.get_user", AsyncMock(return_value=test_data)), \
            patch("main.db_fav_manager.get_message_text",
                  AsyncMock(return_value={"text": "test", "character": 1})):
        await get_favorites(mock_message)

        assert mock_message.answer.call_count == 4


@pytest.mark.asyncio
async def test_process_message_request_random(mock_message):
    state = MagicMock(spec=FSMContext)
    state.update_data = AsyncMock()

    with patch("random.randint", return_value=5):
        await process_message_request_random(mock_message, state)

        state.update_data.assert_called_once_with(character_id=5)
        mock_message.answer.assert_called_once()



@pytest.mark.asyncio
async def test_handle_unknown(mock_message):
    await handle_unknown(mock_message)
    mock_message.answer.assert_called_with("🔍 Вы пока не сделали выбор. Нажмите кнопки ниже! 👇")

@pytest.mark.asyncio
async def test_new_message_request_invalid_data(mock_message):
    mock_message.web_app_data = WebAppData(
        data='{invalid json}',
        button_text="Choose Character"
    )
    state = MagicMock(spec=FSMContext)
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()

    await new_message_request(mock_message, state)

    mock_message.answer.assert_called_once_with("⚠️ Ошибка обработки выбора. Попробуйте еще раз!")
    state.update_data.assert_not_called()
    state.set_state.assert_not_called()





@pytest.mark.asyncio
@patch("main.get_voice", return_value=("dummy", "dummy", "path/to/audio.wav"))
async def test_process_message_request(mock_get_voice, mock_message):
    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={"character_id": 2})
    state.set_state = AsyncMock()

    with patch("main.FSInputFile"), \
            patch("main.db_fav_manager.save_message", AsyncMock()), \
            patch("asyncio.sleep", AsyncMock()):
        await process_message_request(mock_message, state)

        mock_message.answer_voice.assert_not_called()

@pytest.mark.asyncio
async def test_cmd_start(mock_message):
    await cmd_start(mock_message)
    mock_message.answer.assert_called_once_with(welcome_message(mock_message), reply_markup=mock_message.answer.call_args[1]["reply_markup"])

@pytest.mark.asyncio
async def test_handle_unknown_message(mock_message):
    await handle_unknown(mock_message)
    mock_message.answer.assert_called_once_with(didnt_choose_text)

@pytest.mark.asyncio
async def test_new_message_request_no_web_data(mock_message):
    mock_message.web_app_data = None
    state = MagicMock(spec=FSMContext)

    await new_message_request(mock_message, state)

    mock_message.answer.assert_called_once_with(didnt_choose_text)


@pytest.mark.asyncio
async def test_process_message_request_random_voice(mock_message):
    state = MagicMock(spec=FSMContext)
    state.update_data = AsyncMock()

    with patch("random.randint", return_value=7):
        await process_message_request_random(mock_message, state)

        state.update_data.assert_called_once_with(character_id=7)
        mock_message.answer.assert_called_once()

def test_generate_safe_id():
    input_string = "test_string"
    result = generate_safe_id(input_string)

    assert isinstance(result, str)
    assert len(result) == 32


@pytest.mark.asyncio
@patch("main.FSInputFile")
async def test_get_favorites_with_audio(mock_fsinput, mock_message):
    test_data = {"favourite_messages": ["path/to/audio.wav"]}

    with patch("main.db_manager.get_user", AsyncMock(return_value=test_data)), \
            patch("main.db_fav_manager.get_message_text",
                  AsyncMock(return_value={"text": "test message", "character": 2})):
        await get_favorites(mock_message)

        assert mock_message.answer.call_count > 1

@pytest.mark.asyncio
async def test_handle_specific_types_non_text(mock_message):
    mock_message.content_type = "photo"

    await handle_specific_types(mock_message)

    mock_message.answer.assert_called_once_with(specific_type_text)

