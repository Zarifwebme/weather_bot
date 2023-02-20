import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Salom!\n"
                         "Viloyat va shahar nomlarini kiriting\n"
                         "Masalan: Toshkent")


@dp.message_handler(commands=["help"])
async def start_command(message: types.Message):
    await message.answer("Muamo va xatoliklar sezsangiz\n"
                         "Ushbu kontaktga bog'laning\n"
                         "https://t.me/bakhtiyorovzarif"
                         )


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Yaxshi \U00002600",
        "Clouds": "Bulutli \U00002601",
        "Rain": "Yomg'rli \U00002614",
        "Drizzle": "Yomg'rli \U00002614",
        "Thunderstorm": "Bo'ron \U000026A1",
        "Snow": "Qorli \U0001F328",
        "Mist": "Tuman \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']  # hozirgi ob hovo

        weather_descrition = data["weather"][0]["main"]
        if weather_descrition in code_to_smile:
            wd = code_to_smile[weather_descrition]
        else:
            wd = "Derazadan qarang ob-hovo qandayligini aniqlay olamdim"

        humidity = data['main']['humidity']  # namlik
        pressure = data['main']['pressure']  # bosim
        wind = data['wind']['speed']  # shamol tezligi
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])  # quyosh chiqishi vaqti
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])  # quyosh botishi
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])  # kun qismi

        await message.reply(f"Hozirgi vaqt: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                            f"Makon: {city}\n "
                            f"Gradus: {cur_weather} C° {wd}\n "
                            f"Namlik {humidity}%\n "
                            f"Bosim: {pressure}\n"
                            f"Shamol tezligi: {wind}\n "
                            f"Quyosh chiqishi: {sunrise_timestamp}\n "
                            f"Quyosh botishi: {sunset_timestamp}\n"
                            f"Kun qismi: {length_of_the_day}")

    except:
        await message.reply("\U00002620 Xato kiritdingiz \U00002620")


if __name__ == "__main__":
    executor.start_polling(dp)
