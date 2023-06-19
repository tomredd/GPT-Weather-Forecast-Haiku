from PIL import Image, ImageDraw, ImageFont
import configparser

# Create an instance of the ConfigParser class
config = configparser.ConfigParser()

# Read the INI file
config.read('config.ini')

# Define the dimensions of the display
DISPLAY_WIDTH = 300
DISPLAY_HEIGHT = 400

# Define the file path of the JPG image
IMAGE_FILE = config.get('FILE_PATH', 'input_image')

# Define the file path of the text file
TEXT_FILE = config.get('FILE_PATH', 'input_haiku')

# Define the file path to save the output JPG image
OUTPUT_IMAGE_FILE = config.get('FILE_PATH', 'output_image')

# Define the border size around the text
TEXT_BORDER = 10

# Load the image using PIL
image = Image.open(IMAGE_FILE)

# Resize the image to fill the top two thirds of the display
image = image.resize((DISPLAY_WIDTH, 2 * DISPLAY_HEIGHT // 3))

# Load the text from the file
with open(TEXT_FILE, "r") as file:
    lines = file.readlines()

# Calculate the maximum font size to fit the text within the display area
max_font_size = 72

# Find the largest font size that fits the text within the display area
for font_size in range(max_font_size, 0, -1):
    font = ImageFont.truetype(config.get('FILE_PATH', 'font_path'), font_size)
    draw = ImageDraw.Draw(image)

    # Calculate the position to display the text in the bottom third with the desired border
    text_x = TEXT_BORDER
    text_y = (2 * DISPLAY_HEIGHT // 3) + TEXT_BORDER

    # Check if all lines of text fit within the display area with the desired border
    text_rects = []
    for line in lines:
        line = line.strip()
        text_bbox = draw.textbbox((text_x, text_y), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_rects.append((text_width, text_height))
        text_y += text_height

    if all(rect[0] <= DISPLAY_WIDTH - 2 * TEXT_BORDER for rect in text_rects) and \
            text_y <= DISPLAY_HEIGHT - TEXT_BORDER:
        break

# Create a new image with the desired dimensions and paste the resized image onto it
output_image = Image.new("RGB", (DISPLAY_WIDTH, DISPLAY_HEIGHT), (0, 0, 0))
output_image.paste(image, (0, 0))

# Render and display each line of the text on the output image
draw = ImageDraw.Draw(output_image)
text_y = (2 * DISPLAY_HEIGHT // 3) + 2 * TEXT_BORDER  # Adjusted for the border
text_color = (255, 255, 255)  # White color for the text
background_color = (0, 0, 0)  # Black background color
for line in lines:
    line = line.strip()
    text_bbox = draw.textbbox((text_x, text_y), line, font=font)
    draw.rectangle(text_bbox, fill=background_color)
    draw.text((text_x, text_y), line, fill=text_color, font=font)
    text_y += text_bbox[3] - text_bbox[1]

# Save the displayed image as a new JPG file
output_image.save(OUTPUT_IMAGE_FILE, "JPEG")
