import telebot

TOKEN = "8218056063:AAEq8B0f4zTM10nlr5NBI4bUT9ljp46zl0Y"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Бот работает 🚀\n\nОтправь ИНН."
    )

@bot.message_handler(func=lambda m: True)
def handle_inn(message):

    inn = message.text.strip()

    if not inn.isdigit():
        bot.send_message(
            message.chat.id,
            "ИНН должен содержать только цифры."
        )
        return

    bot.send_message(
        message.chat.id,
        f"Поиск информации по ИНН: {inn}"
    )

bot.infinity_polling()
