import requests
from get_token import get_token

def synthesize_speech(text, voice):
    """
    Функция для синтеза речи.
    :param text: Текст для синтеза.
    :param voice: Голос для синтеза (например, Nec_24000).
    :return: Сгенерированный аудиофайл в бинарном виде.
    """
    token = get_token()
    url = "https://smartspeech.sber.ru/rest/v1/text:synthesize"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/text",  # По умолчанию используем обычный текст (UTF-8)
        "Accept-Charset": "UTF-8"
    }

    # Параметры запроса: голос и формат аудио
    params = {
        "voice": voice,
        "format": "wav16"  # По умолчанию используем формат wav16
    }

    # Отправляем текст напрямую в теле запроса
    body = text

    # Отправка POST-запроса с текстом в body
    response = requests.post(url, headers=headers, params=params, data=body.encode('utf-8'), verify=False)

    if response.status_code == 200:
        return response.content  # Возвращаем бинарные данные аудиофайла
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")


# Пример использования
audio_data = synthesize_speech(
    text="Привет, мир!",  # Текст для синтеза
    voice="Nec_24000"     # Голос для синтеза
)

# Пример сохранения полученного аудиофайла (опционально)
with open("output.wav", "wb") as f:
    f.write(audio_data)
