from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_socketio import SocketIO, send
import requests
import datetime as dt
import googletrans
from googletrans import Translator
from weather import get_weather_results, kelvin_to_celsius_fahrenheit 

from translate import checkLanguageCode, translate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'esunsecret1234'
socketio = SocketIO(app)

#Controladores de ruta que definen la lógica que se ejecutará cuando se acceda a una determinada URL
@app.route('/', methods=['GET', 'POST'])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("username")

        if not name:
            return render_template("home.html", error="Please enter a name.", name=name)

        session["name"] = name  # Store users data temporal

        return redirect(url_for("chat"))

    return render_template("home.html", boolean=True)


@app.route("/chat")
def chat():
    # Only available to enter if you have gone through the home page first
    if chat is None or session.get("name") is None:
        return redirect(url_for("home"))

    return render_template("chat.html")


@socketio.on('get_weather')
def get_weather(city):
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "f1b1af4594b289ef32467e44f61e0830"
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    error=False

    weather_info = requests.get(url)
    print(weather_info)
    if weather_info.status_code == 404:
        error= True
        data={}
    else:
        response= weather_info.json()
        data = {
        'temp_kelvin': response['main']['temp'],
        'temp_celsius': kelvin_to_celsius_fahrenheit(response['main']['temp'])[0],
        'temp_fahrenheit': kelvin_to_celsius_fahrenheit(response['main']['temp'])[1],
        'feels_like_kelvin': response['main']['feels_like'],
        'feels_like_celsius': kelvin_to_celsius_fahrenheit(response['main']['feels_like'])[0],
        'feels_like_fahrenheit': kelvin_to_celsius_fahrenheit(response['main']['feels_like'])[1],
        'wind_speed': response['wind']['speed'],
        'humidity': response['main']['humidity'],
        'description': response['weather'][0]['description'],
        'sunrise_time': str(dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])),
        'sunset_time': str(dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone']))
        }
    return error, data


@socketio.on("message")  # Aqui haurem de agafar nosaltres el text de weather
def get_data(data):
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content)
    input_string = data["data"].lower()
    print(f"{input_string}")
    words = input_string.split()
    print(words)
    if words[0]=='weather':
        if len(words) >= 2:
            city = ''
            for i in range(1, len(words)):
                city += words[i]+' '
            print(city)
            error, weather_data= get_weather(city)
            content = {
                "name": 'Server',
                "message": get_weather_results(city, weather_data, error)
            }
            send(content)
            print(f"Weather data: {get_weather_results(city,weather_data, error)}")
        pass

    elif words[0]=='translate':
        text_to_translate = ''
        for i in range(3, len(words)):
            text_to_translate += words[i]+' '
        lang= words[2]
        #print(text_to_translate)
        #print(lang)
        if checkLanguageCode(lang):
            translation = translate(text_to_translate, lang)
            msg= translation.text
        else:
            link = "https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages "
            link_text = "Language not found. You can find the available languages by clicking here."
            msg = f'<a href="{link}">{link_text}</a>'
        
        content = {
        "name": 'Server',
        "message": msg
        }
        send(content)
        pass
    
    else: 
        content = {
        "name": 'Server',
        "message": "Hi! How can I help you out? You can say: \n Weather [city] --> To know the weather in the selected city\n Translate to [language code] [text to translate] --> To translate the text you want\n Some common language codes are:\n EN (English)\n ES (Spanish)\n DE (German)\n FR (French)"          }
        send(content)


    print(f"{session.get('name')} said: {data['data']}")


if __name__ == '__main__':
    # run our flask application, and rerun if there's any changes
    socketio.run(app, debug=True)
