# WeatherHaiku
This is a project I've created to learn how to code in python. It uses the OpenAI large language models to generate a haiku and relevant picture based on the weather forecast for the day. The final image is displayed on an e-ink display.

## Hardware
### Pimoroni Inky wHAT – Black/White/Red
Inky wHAT is a 400x300 pixel electronic paper display for Raspberry Pi. Installation instructions are:
https://github.com/pimoroni/inky

### Raspberry Pi Zero W
Any raspberry pi model will do but since this code isn't resource intensive, I would suggest an older model you might have lying around. It might be easier to setup the pi to run headless so you can ssh into it. You will need to install a number of packages by running the following commands:
- pip install openai
- pip3 install inky[rpi,example-depends]

## Software
Rather than one script, I have created several to allow the user to play around without the different elements. These five files are:
- Application.py: This is a simple script that runs the other python files in sequence. It also makes scheduling with Cron a bit easier (see below).
- Haiku_Image_Generator.py: This script does most of the heavy lifting. It generates a weather forecast for your town and then uses this as a prompt to generate Haiku from OpenAI's gpt model and an image from their Dall-E model.
- Image_Creator: This combines the haiku and image into what will eventually be displayed on the Inky wHAT.
- PrintInky.py: This displays the final image on the Inky wHAT.
- config.ini: VERY IMPORTANT, you need to insert your API keys, location, and file pathways into this file.

## API Keys
### Open Weather Map
You can can sign-up for the Open Weather Map API key here: https://openweathermap.org/api

### OpenAI API
You can sign-up for an OpenAI API key here: https://platform.openai.com/account/api-keys
Note: there is a limited trial, afterwards you will need to enter payment details to use this API.

## Font
You can play around with different fonts, but I quite like LibreBaskerville-Regular: https://github.com/impallari/Libre-Baskerville

## Schedule using Crontab
To schedule this to run on a regular basis (daily) you can schedule the Application.py script in Cron. You can learn how to do this here:
https://bc-robotics.com/tutorials/setting-cron-job-raspberry-pi/

Becasue the Application is dependent on the config.ini file, I found that it was neccisary to use the folloing command in cron. Change the filepath as needed.

cd /home/pi/WeatherHaiku && python3 Application.py

## What it looks like
This is what it looks like on the Inky wHAT.

![20230619_064047635_iOS](https://github.com/tomredd/GPT-Weather-Forecast-Haiku/assets/6317074/735e7917-364b-4640-98cb-25ca5e3173c1)
