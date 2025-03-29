from typing import TypedDict


# Здесь находятся все представленные модели с их настройками

class ModelParams(TypedDict):
    name: str  # название модели как в RVC модели
    speed: int  # скорость воспроизведения [-50;50]
    input_text: str  # текст для конвертации
    edge_voice: str  # первоначальный голос: ("ru-RU-DmitryNeural-Male", "ru-RU-SvetlanaNeural-Female")
    transpose: float  # смена октавы (одна октава -- 12)
    method: str  # (метод конвертации ("rmvpe", "pm")
    index_rate: float  # степень наложения голоса [0;1]
    protect: float  # степень заимствования голоса [0;0.5]


voices: dict[int, ModelParams] = {
    1: {
        "name": "Пудж",
        "speed": -10,
        "input_text": "",
        "edge_voice": "ru-RU-DmitryNeural-Male",
        "transpose": -8,
        "method": "rmvpe",
        "index_rate": 0,
        "protect": 0
    },
    2: {
        "name": "Шрек",
        "speed": 0,
        "input_text": "",
        "edge_voice": "ru-RU-DmitryNeural-Male",
        "transpose": 3.5,
        "method": "rmvpe",
        "index_rate": 1,
        "protect": 0
    },
    3: {
        "name": "Диппер",
        "speed": 0,
        "input_text": "",
        "edge_voice": "ru-RU-DmitryNeural-Male",
        "transpose": 8,
        "method": "rmvpe",
        "index_rate": 1,
        "protect": 0.33
    },
    4: {
        "name": "Мейбл",
        "speed": 0,
        "input_text": "",
        "edge_voice": "ru-RU-SvetlanaNeural-Female",
        "transpose": 14,
        "method": "rmvpe",
        "index_rate": 0,
        "protect": 0.5
    },
    5: {
        "name": "Апвоут",
        "speed": 30,
        "input_text": "",
        "edge_voice": "ru-RU-DmitryNeural-Male",
        "transpose": 3,
        "method": "rmvpe",
        "index_rate": 0,
        "protect": 0
    },
    6: {
        "name": "ДональдДак",
        "speed": 0,
        "input_text": "",
        "edge_voice": "ru-RU-DmitryNeural-Male",
        "transpose": 10,
        "method": "rmvpe",
        "index_rate": 1,
        "protect": 0.5
    },
    7: {
        "name": "Крош",
        "speed": 20,
        "input_text": "",
        "edge_voice": "ru-RU-DmitryNeural-Male",
        "transpose": 14,
        "method": "rmvpe",
        "index_rate": 0.23,
        "protect": 0
    },
    8: {
        "name": "Геральт",
        "speed": 0,
        "input_text": "",
        "edge_voice": "ru-RU-DmitryNeural-Male",
        "transpose": -2,
        "method": "rmvpe",
        "index_rate": 0,
        "protect": 0
    },
    9: {
        "name": "ИванУргант",
        "speed": 10,
        "input_text": "",
        "edge_voice": "ru-RU-DmitryNeural-Male",
        "transpose": 1.5,
        "method": "rmvpe",
        "index_rate": 0,
        "protect": 0
    }

}
