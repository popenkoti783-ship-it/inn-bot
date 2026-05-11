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
    url = f"https://bo.nalog.ru/search-proc.json?query={inn}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        data = response.json()

        if "suggestions" not in data:
            return "Компания не найдена."

        if len(data["suggestions"]) == 0:
            return "Компания не найдена."

        company = data["suggestions"][0]

        name = company.get("name", "Нет названия")
        ogrn = company.get("ogrn", "Нет ОГРН")
        address = company.get("address", "Нет адреса")

        return f"""
🏢 Компания:
{name}

🆔 ИНН:
{inn}

📄 ОГРН:
{ogrn}

📍 Адрес:
{address}
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


print("Бот запущен...")

bot.infinity_polling()
