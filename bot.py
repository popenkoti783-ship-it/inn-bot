import telebot
import requests

TOKEN = "8218056063:AAEq8B0f4zTM10nlr5NBI4bUT9ljp46zl0Y"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Отправь ИНН компании"
    )

@bot.message_handler(func=lambda message: True)
def inn_search(message):

    inn = message.text.strip()

    if not inn.isdigit():
        bot.send_message(
            message.chat.id,
            "ИНН должен содержать только цифры"
        )
        return

    url = f"https://egrul.itsoft.ru/{inn}.json"

    try:

        response = requests.get(url)

        data = response.json()

        if "СвЮЛ" not in data:

            bot.send_message(
                message.chat.id,
                "Компания не найдена"
            )
            return

        company = data["СвЮЛ"]

        name = company.get("СвНаимЮЛ", "Нет данных")

        address = "Нет данных"

        if "СвАдресЮЛ" in company:
            address = str(company["СвАдресЮЛ"])

        text = (
            f"🏢 {name}\n\n"
            f"ИНН: {inn}\n\n"
            f"📍 Адрес:\n{address}"
        )

        bot.send_message(
            message.chat.id,
            text
        )

    except Exception as e:

        bot.send_message(
            message.chat.id,
            f"Ошибка: {e}"
        )

bot.infinity_polling()
