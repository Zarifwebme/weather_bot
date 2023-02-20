import requests
import datetime
from pprint import pprint
from config import open_weather_token

def get_weather(city, open_weather_token):

    code_to_smile = {
        "Clear": "Yaxshi \U00002600",
        "Clouds": "Bulutli \U00002601",
        "Rain": "Yomg'rli \U00002614",
        "Drizzle": "YYomg'rli \U00002614",
        "Thunderstorm": "Bo'ron \U000026A1",
        "Snow": "Qorli \U0001F328",
        "Mist": "Tuman \U0001F32B"
    }


    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        pprint(data)

        city = data['name']
        cur_weather = data['main']['temp']        #hozirgi ob hovo

        weather_descrition = data["weather"][0]["main"]
        if weather_descrition in code_to_smile:
            wd = code_to_smile[weather_descrition]
        else:
            wd = "Derazadan qarang ob-hovo qandayligini anialy olamdim"

        humidity = data['main']['humidity']         #namlik
        pressure = data['main']['pressure']         #bosim
        wind = data['wind']['speed']                #shamol tezligi
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])  #quyosh chiqishi vaqti
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])    #quyosh botishi
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"]) #kun qismi
        country = data[""]
        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Makon: {city}\n Gradus: {cur_weather} C° {wd}\n "
              f"Namlik {humidity}%\n Bosim: {pressure}\n"
              f"Shamol tezligi: {wind}\n Quyosh chiqishi: {sunrise_timestamp}\n Quyosh botishi: {sunset_timestamp}\n"
              f"Kun qismi: {length_of_the_day}")



    except Exception as ex:
        print(ex)
        print("Shahar nomini tekshirish")

def main():
    city = input("Shaharni kiriting: ")
    get_weather(city, open_weather_token)

if __name__ == "__main__":
    main()