from gradio_client import Client
from TTS import models
client = Client("http://127.0.0.1:7860/")

voice_data_male = {"Джарвис": "Jarvis", "Путин": "Putin_model_200", "Валакас": "Valakas_350"}
voice_data_female = {"Квопа": "Qop_model_100"}


def is_right_voice(voice):
    return voice in voice_data_male or voice in voice_data_female


def is_male_or_female(voice):  # True - male, False - female
    if not is_right_voice(voice):
        return Exception("Нет такого голоса!")
    if voice in voice_data_male:
        return voice_data_male, "ru-RU-DmitryNeural-Male"
    return voice_data_female, "ru-RU-SvetlanaNeural-Female"


def split_text(input_text):
    before_colon, after_colon = input_text.split(":", 1)
    before_colon = before_colon.strip()
    after_colon = after_colon.strip()
    return before_colon, after_colon


def get_voice(voice_name, text):
    if not is_right_voice(voice_name):
        return Exception
    voice_data, voice = is_male_or_female(voice_name)

    result = client.predict(
        voice_data[voice_name],
        0,
        text,
        voice,
        0,
        "rmvpe",
        0,
        0,
        fn_index=0
    )
    return result
