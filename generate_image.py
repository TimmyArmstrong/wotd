import json
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Load location data from JSON file
with open("location_data_output.json", "r") as f:
    data = json.load(f)

# Extract values
city = data["city"]
state = data["state"]
region = data["region"]
altitude = data["altitude_metres"]

# Load weather summary sentence from JSON file
with open("weather_output.json", "r") as f:
    weather_data = json.load(f)
sentence = weather_data.get("weather_summary", "")

# Construct text
title = city
subtitle = f"{state}, {region}"
body_text = f"Situated {altitude} metres above sea level.\n{sentence}"

# Image size
WIDTH, HEIGHT = 296, 128

# Create a blank 1-bit image (white background)
img = Image.new('1', (WIDTH, HEIGHT), 1)
draw = ImageDraw.Draw(img)

def load_font(filename, size):
    return ImageFont.truetype(filename, size)

def get_text_height(font, text):
    bbox = font.getbbox(text)
    return bbox[3] - bbox[1]

def fit_text_to_width(text, font_name, max_width, initial_size):
    size = initial_size
    while size > 6:
        font = load_font(font_name, size)
        bbox = font.getbbox(text)
        if bbox[2] - bbox[0] <= max_width:
            return font
        size -= 1
    return load_font(font_name, size)

# Margins and max width
SIDE_MARGIN = 5
max_text_width = WIDTH - 2 * SIDE_MARGIN

# Load fonts with fitting sizes for title and subtitle
font_title = fit_text_to_width(title, "DejaVuSans-Bold.ttf", max_text_width, 24)
font_subtitle = fit_text_to_width(subtitle, "DejaVuSans.ttf", max_text_width, 16)
font_body = load_font("DejaVuSans", 12)

y = 5

# Draw title with spacing after
draw.text((SIDE_MARGIN, y), title, font=font_title, fill=0)
y += get_text_height(font_title, title) + 10

# Draw subtitle with spacing after
draw.text((SIDE_MARGIN, y), subtitle, font=font_subtitle, fill=0)
y += get_text_height(font_subtitle, subtitle) + 10

# Wrap body text (including weather sentence) and draw lines with spacing
wrapper = textwrap.TextWrapper(width=45)
lines = wrapper.wrap(body_text)[:5]  # Increased lines to accommodate more text

for line in lines:
    draw.text((SIDE_MARGIN, y), line, font=font_body, fill=0)
    y += get_text_height(font_body, line) + 6

# Save image
img = img.convert("1") 
img.save("epaper_output.bmp","BMP")
