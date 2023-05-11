def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit


def get_weather_results(city, data, error=False):
    if error==True:
        result=f"City not found, try again\n Remember to type in: Weather [city]\n"
    else:
        temp_celsius = data['temp_celsius']
        temp_fahrenheit = data['temp_fahrenheit']
        feels_like_celsius = data['feels_like_celsius']
        feels_like_fahrenheit = data['feels_like_fahrenheit']
        humidity = data['humidity']
        wind_speed = data['wind_speed']
        description = data['description']
        sunrise_time = data['sunrise_time']
        sunset_time = data['sunset_time']
        sunrise_time = data['sunrise_time']

        result = f"Temperature in {city}: {temp_celsius:.2f}ºC or {temp_fahrenheit:.2f}ºF \n" \
           f" Temperature in {city} feels like: {feels_like_celsius:.2f}ºC or {feels_like_fahrenheit:.2f}ºF \n" \
           f" Humidity in {city}: {humidity}% \n" \
           f" Wind Speed in {city}: {wind_speed}m/s \n" \
          f" General Weather in {city}: {description} \n" \
          f" Sun rises in {city}: {sunrise_time} local time. \n" \
          f" Sun sets in {city}: {sunset_time} local time."
    return result

