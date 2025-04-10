from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State, StatesGroup


class MessageCallback(CallbackData, prefix="favorite"):
    action: str
    message_file: str
    text_id: str


class MessageStates(StatesGroup):
    waiting_for_message_request = State()
    selected_character = State()
    waiting_for_favorite_messages = State()


class FeedbackStates(StatesGroup):
    waiting_for_feedback = State()
