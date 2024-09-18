import openai
import telebot
import logging
import os
import time
from dotenv import load_dotenv

# Загрузка env
load_dotenv()

# Установка API-ключа
openai.api_key = os.getenv('OPENAI_API_KEY')
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

# Настройка логирования
log_dir = os.path.join(os.path.dirname(__file__), 'ChatGPT_Logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(filename=os.path.join(log_dir, 'error.log'), level=logging.ERROR,
                    format='%(levelname)s: %(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет!\nЯ ChatGPT 3.5 Telegram Bot 🤖\nЗадай мне любой вопрос и я постараюсь на него ответить')

def generate_response(prompt):
    try:
        print(f"Generating response for prompt: {prompt}")  # Печать запроса
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(f"Response received: {response}")  # Печать ответа
        content = response['choices'][0]['message']['content']
        print(f"Response content: {content}")  # Печать содержимого ответа
        return content
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        print(f"Error generating response: {e}")  # Печать ошибки
        return "Извините, возникла ошибка при обработке вашего запроса."

@bot.message_handler(commands=['bot'])
def command_message(message):
    print(f"Received command message: {message.text}")  # Печать команды
    prompt = message.text[len('/bot '):]
    response = generate_response(prompt)
    bot.reply_to(message, text=response)

@bot.message_handler(func=lambda _: True)
def handle_message(message):
    print(f"Received message: {message.text}")  # Печать текст сообщения
    prompt = message.text
    response = generate_response(prompt)
    bot.send_message(chat_id=message.from_user.id, text=response)

print('ChatGPT Bot is working')

while True:
    try:
        bot.polling()
    except (telebot.apihelper.ApiException, ConnectionError) as e:
        logging.error(f"Polling error: {e}")
        print(f"Polling error: {e}")  # Печать ошибки при поллинге
        time.sleep(5)
