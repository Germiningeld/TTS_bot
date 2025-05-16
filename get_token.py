import requests
import base64
import uuid
import json
import os
import time
import config as conf

TOKEN_FILE = "token_data.json"

# Параметры для авторизации
client_id = conf.client_id
client_secret = conf.client_secret
auth_url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
scope = 'SALUTE_SPEECH_PERS'  # или другой scope в зависимости от проекта


# Функция для получения нового токена
def get_new_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    rquid = str(uuid.uuid4())
    headers = {
        'Authorization': f'Basic {auth_base64}',
        'RqUID': rquid,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'scope': scope
    }

    response = requests.post(auth_url, headers=headers, data=data, verify=False)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info.get('access_token')
        expires_at = token_info.get('expires_at')

        # Сохраняем токен и время истечения в файл
        with open(TOKEN_FILE, "w") as token_file:
            json.dump({"access_token": access_token, "expires_at": expires_at}, token_file)

        return access_token
    else:
        raise Exception(f"Error getting token: {response.status_code}, {response.text}")


# Функция для загрузки токена из файла или получения нового
def get_token():
    # Проверяем, есть ли сохранённый токен
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as token_file:
            token_data = json.load(token_file)
            current_time = int(time.time() * 1000)  # Текущее время в миллисекундах

            # Проверяем, не истек ли токен
            if current_time < token_data.get("expires_at"):
                return token_data.get("access_token")

    # Если токен истёк или его нет, получаем новый
    print("No valid token found, getting a new one...")
    return get_new_token()


