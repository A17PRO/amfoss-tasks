from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageFilter
from google import genai
from dotenv import load_dotenv
from datetime import datetime
'''
with open("to-do-list.txt", "r") as file:
    content = file.read()
    print(content)
'''
time = datetime.now().strftime("%H:%M:%S")
print(time)

canvas = Image.new("RGB", (1920, 1080), ImageColor.getrgb("#000000"))

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)

draw = ImageDraw.Draw(canvas)
draw.text((1600, 100), time, font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30), fill=(255, 255, 255))

wallpaper_path = "current_wallpaper.jpg"
canvas.save(wallpaper_path)
print(f"Saved successfully to {wallpaper_path}")