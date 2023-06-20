import requests
import json
import openai
import os
import configparser
from datetime import datetime

# Create an instance of the ConfigParser class
config = configparser.ConfigParser()

# Read the INI file
config.read('config.ini')

openai.api_key = config.get('API', 'openai_API')
API_KEY = config.get('API', 'openweathermap_API')
CITY_NAME = config.get('LOCATION', 'location')
FORECAST_URL = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY_NAME}&appid={API_KEY}'

# Send a GET request to retrieve the daily forecast
response_forecast = requests.get(FORECAST_URL)
data_forecast = json.loads(response_forecast.text)

# Extract relevant daily forecast information (e.g., for the next day)
daily_temperature = data_forecast['list'][0]['main']['temp']
daily_humidity = data_forecast['list'][0]['main']['humidity']
daily_description = data_forecast['list'][0]['weather'][0]['description']
daily_temp_min = data_forecast['list'][0]['main']['temp_min']
daily_temp_max = data_forecast['list'][0]['main']['temp_max']

# Check if rain data is available
if 'rain' in data_forecast['list'][0]:
    rain = data_forecast['list'][0]['rain']
else:
    rain = {}

# Check if snow data is available
if 'snow' in data_forecast['list'][0]:
    snow = data_forecast['list'][0]['snow']
else:
    snow = {}

# Check if weather alerts data is available
if 'alerts' in data_forecast:
    alerts = data_forecast['alerts']
else:
    alerts = []

# Convert daily temperature from Kelvin to Celsius
daily_temperature = daily_temperature - 273.15
daily_temp_min = daily_temp_min - 273.15
daily_temp_max = daily_temp_max - 273.15

# Get the date of the forecast
forecast_date = datetime.fromtimestamp(data_forecast['list'][0]['dt']).strftime('%Y-%m-%d')

# Create a human-readable sentence with weather information
weather_sentence = f"Daily forecast for {CITY_NAME} on {forecast_date}: Temperature is {daily_temperature:.2f}°C, with a minimum of {daily_temp_min:.2f}°C and a maximum of {daily_temp_max:.2f}°C. Humidity is {daily_humidity}%. The weather is {daily_description}."

# Add rain information if available
if rain:
    weather_sentence += f" Expect {rain} mm of rain."

# Add snow information if available
if snow:
    weather_sentence += f" Expect {snow} mm of snow."

# Add weather alerts if available
if alerts:
    weather_sentence += " Weather alerts:"
    for alert in alerts:
        event = alert['event']
        start = datetime.fromtimestamp(alert['start']).strftime('%Y-%m-%d %H:%M:%S')
        end = datetime.fromtimestamp(alert['end']).strftime('%Y-%m-%d %H:%M:%S')
        weather_sentence += f" {event} from {start} to {end}."

# Print the combined weather sentence
print(weather_sentence)

#HAIKU GENERATOR 
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You write one haiku based on the weather forecast for the day. You prioritise the description of the weather but if there is a lot of rain, the temperature is extreme for the day, based on the location and time of year, or there is a weather warning, you write about that."},
        {"role": "user", "content": weather_sentence}
    ]
)

# Extract the assistant's reply from the response
assistant_reply = response['choices'][0]['message']['content']

# Print the assistant's reply
print(assistant_reply)

# Save the response to a text file
filename = "haiku.txt"
with open(filename, "w") as file:
    file.write(assistant_reply)
    

#IMAGE GENERATOR    
# The text prompt you want to use to generate an image
prompt = "A woodblock inspired by Katsushika Hokusai that uses only black white and red block colors based on the following description:" + daily_description

print(prompt)

# Generate an image
response = openai.Image.create(
    prompt=prompt,
    model="image-alpha-001",
    size="512x512",
    response_format="url"
)

# Get the URL of the generated image
image_url = response["data"][0]["url"]

# Save the image as a PNG file
save_file_path = "generated_image.png"

response = requests.get(image_url, stream=True)
if response.status_code == 200:
    with open(save_file_path, 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
    print(f"Image downloaded successfully and saved as {save_file_path}")
else:
    print("Failed to download image.")
