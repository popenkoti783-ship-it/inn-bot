import telebot
import requests

TOKEN = "8218056063:AAEq8B0f4zTM10nlr5NBI4bUT9ljp46zl0Y"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Бот работает 🚀\n\nОтправь ИНН компании."
    )


def get_company_info(inn):
    url = f"https://egrul.itsoft.ru/{inn}.json"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return "Компания не найдена."

        data = response.json()

        if "СвЮЛ" not in data:
            return "Информация не найдена."

        company = data["СвЮЛ"]

        name = company.get("СвНаимЮЛ", {}).get("НаимЮЛПолн", "Нет названия")

        ogrn = company.get("ОГРН", "Нет ОГРН")

        return f"""
🏢 Компания:
{name}

🆔 ИНН:
{inn}

📄 ОГРН:
{ogrn}
"""

    except Exception as e:
        return f"Ошибка: {e}"


@bot.message_handler(func=lambda m: True)
def handle_inn(message):
    inn = message.text.strip()

    if not inn.isdigit():
        bot.send_message(
            message.chat.id,
            "ИНН должен содержать только цифры."
        )
        return

    result = get_company_info(inn)

    bot.send_message(
        message.chat.id,
        result
    )


bot.infinity_polling()
