from gradio_client import Client
from TTS.models import voices
client = Client("http://127.0.0.1:7860/")

def get_voice(voice_id, text):
    voice_data = voices[voice_id]

    result = client.predict(
        voice_data["name"],
        voice_data["speed"],
        text,
        voice_data["edge_voice"],
        voice_data["transpose"],
        voice_data["method"],
        voice_data["index_rate"],
        voice_data["protect"],
        fn_index=0
    )
    return result
