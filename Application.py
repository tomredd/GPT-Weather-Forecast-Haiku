import subprocess
import configparser

# Create an instance of the ConfigParser class
config = configparser.ConfigParser()

# Read the INI file
config.read('config.ini')

# Run first script
print("Running Haiku_Image_Generator...")
subprocess.run(["python3", config.get('FILE_PATH', 'Haiku_Image_Generator')])
print("Haiku_Image_Generator finished.")

# Run second script
print("Running Image_Creator...")
subprocess.run(["python3", config.get('FILE_PATH', 'Image_Creator')])
print("Image_Creator finished.")

# Run third script
print("Running PrintInky...")
subprocess.run(["python3", config.get('FILE_PATH', 'PrintInky')])
print("PrintInky finished.")
