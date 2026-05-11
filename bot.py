import telebot
from openai import OpenAI

TOKEN = "8218056063:AAEq8B0f4zTM10nlr5NBI4bUT9ljp46zl0Y"
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)

client = OpenAI(
    api_key=OPENAI_API_KEY
)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🤖 CRM AI Assistant запущен.\n\nНапиши любой вопрос."
    )

@bot.message_handler(func=lambda message: True)
def chat(message):

    user_text = message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ты CRM AI Assistant. Отвечай кратко и полезно."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        answer = response.choices[0].message.content

        bot.send_message(
            message.chat.id,
            answer
        )

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"Ошибка: {e}"
        )

bot.infinity_polling()
