import json
import azure.functions as func
import logging
import requests
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="GetWeatherByZipCode")
def GetWeatherByZipCode(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    zipCode = req.params.get('zipCode')
    if not zipCode:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            zipCode = req_body.get('zipCode')

    if zipCode:
        # Call the weather API to get the weather for the passed in zip code
        weather = get_weather(zipCode)

        if weather:
            weather_json = {
                "temperature": weather.temperature,
                "location": weather.location,
                "wind_speed": weather.wind_speed,
                "wind_direction": weather.wind_direction,
                "conditions": weather.conditions
            }
            return func.HttpResponse(json.dumps(weather_json), mimetype="application/json")
        else:
            return func.HttpResponse(f"Unable to retrieve weather for {zipCode}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a zipCode in the query string or in the request body for a personalized response.",
             status_code=200
        )

def get_weather(zip_code):
    api_key = os.environ.get('WEATHER_API_KEY')
    base_url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()

    if response.status_code == 200:
        # Assuming the API returns temperature in Kelvin
        temperature = data['main']['temp']
        # Convert temperature to Fahrenheit
        temperature = (temperature - 273.15) * 9/5 + 32

        location = data['name']
        wind_speed = data['wind']['speed']
        wind_direction = data['wind']['deg']
        conditions = data['weather'][0]['description']

        weather = Weather(temperature, location, wind_speed, wind_direction, conditions)
        return weather
    else:
        return None

class Weather:
    def __init__(self, temperature, location, wind_speed, wind_direction, conditions):
        self.temperature = temperature
        self.location = location
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.conditions = conditions