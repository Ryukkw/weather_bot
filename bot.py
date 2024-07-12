import telebot
import requests

bot = telebot.TeleBot("TELEGRAM_API_KEY")
API = "openweathermap.org_API_KEY"


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id, "Привет! Напиши название города, а я пришлю тебе погоду в нем!"
    )


@bot.message_handler(content_types=["text"])
def get_weather(message):
    try:
        city = message.text.strip().lower()
        weather_request = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric"
        )
        data = weather_request.json()

        if weather_request.status_code == 200:
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            image = "hot.jpg" if temp >= 10 else "cold.jpg"
            file = open("./" + image, "rb")

            bot.reply_to(
                message, f"Погода в городе: {temp}°C\nОщущается как: {feels_like}°C"
            )
            bot.send_photo(message.chat.id, file)
        else:
            bot.reply_to(message, "Город не найден!")
    except Exception:
        bot.send_message(
            message.chat.id, "Произошла ошибка при получении погоды. Попробуйте позже."
        )


bot.infinity_polling()
