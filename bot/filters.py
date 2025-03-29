from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State, StatesGroup
from bot.texts import *
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Filter


class MessageCallback(CallbackData, prefix="favorite"):
    action: str
    message_file: str



class MessageStates(StatesGroup):
    waiting_for_message_request = State()
    selected_character = State()
    waiting_for_favorite_messages = State()

class MenuButtonFilter(Filter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        if message.text and message.text.startswith('/'):
            return False

        current_state = await state.get_state()

        text_input_states = [
            MessageStates.waiting_for_message_request
        ]

        if current_state in [state.state for state in text_input_states]:
            return True

        menu_buttons = [
            buttons["new_message"],
            buttons["favorite_messages"],
            buttons["message_history"],
            "Отмена",
        ]
        return message.text in menu_buttons
