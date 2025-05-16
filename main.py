import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import telebot
from telebot import types
import config as conf  # Модуль с токенами и словарями
import voice
import os  # Импортируем os для работы с файловой системой
import time

# Получаем список голосов из конфига
voices_dict = conf.voices_dict
TOKEN = conf.bot_token
bot = telebot.TeleBot(TOKEN)

# Переменная для хранения выбранного голоса пользователем
user_data = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     "Привет! Я бот для создания озвучки! Выбери голос, который будет использоваться при создании озвучки:")

    # Создаем клавиатуру с голосами
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    # Добавляем кнопки голосов в два ряда
    buttons = [types.KeyboardButton(voice_name) for voice_name in voices_dict.keys()]
    markup.add(*buttons)

# Обработчик выбора голоса
@bot.message_handler(func=lambda message: message.text in voices_dict.keys())
def handle_voice_choice(message):
    chat_id = message.chat.id
    voice_name = message.text
    user_data[chat_id] = voice_name  # Сохраняем выбранный голос для пользователя

    bot.send_message(chat_id, f"Вы выбрали голос: {voice_name}. Теперь введите текст для озвучки:")


# Обработчик текста для озвучки
@bot.message_handler(func=lambda message: message.chat.id in user_data)
def handle_text_for_speech(message):
    chat_id = message.chat.id
    text = message.text
    voice_name = user_data[chat_id]
    voice_code = voices_dict[voice_name]  # Получаем код голоса из словаря

    try:
        # Генерация аудио через voice.py
        audio_data = voice.synthesize_speech(text, voice_code)

        # Сохраняем аудио во временный файл
        timestamp = int(time.time())
        output_file = f"output_{timestamp}.wav"
        with open(output_file, "wb") as f:
            f.write(audio_data)

        # Отправляем аудио файл
        with open(output_file, 'rb') as audio:
            bot.send_audio(chat_id, audio)

        # Отправляем голосовое сообщение
        with open(output_file, 'rb') as audio:
            bot.send_voice(chat_id, audio)

        # Удаляем временный файл после отправки
        os.remove(output_file)
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка: {str(e)}")


# Запуск бота
if __name__ == '__main__':
    bot.infinity_polling()
